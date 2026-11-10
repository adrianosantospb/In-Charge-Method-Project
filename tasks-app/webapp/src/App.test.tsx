import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";

type Reply = { status: number; body?: unknown };
type Route = (init: RequestInit | undefined) => Reply;

// A fake backend: each test lists the answers it expects for "METHOD /path".
let routes: Record<string, Route>;
let calls: string[];
let contentTypes: Record<string, string | undefined>;

beforeEach(() => {
  calls = [];
  contentTypes = {};
  vi.stubGlobal(
    "fetch",
    vi.fn(async (url: string, init?: RequestInit) => {
      const key = `${init?.method ?? "GET"} ${url}`;
      calls.push(key);
      contentTypes[key] = new Headers(init?.headers).get("Content-Type") ?? undefined;
      const route = routes[key];
      if (!route) throw new Error(`Unexpected request: ${key}`);
      const { status, body } = route(init);
      return new Response(status === 204 ? null : JSON.stringify(body ?? {}), { status });
    }),
  );
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

const alice = { id: "u1", email: "alice@example.com" };
const signedOut: Route = () => ({ status: 401, body: { detail: "Sign in to continue." } });

describe("signing in", () => {
  it("shows the sign-in form when there is no session", async () => {
    routes = { "GET /api/auth/me": signedOut };

    render(<App />);

    expect(await screen.findByRole("heading", { name: "Sign in" })).toBeInTheDocument();
  });

  it("shows the tasks after a correct password", async () => {
    routes = {
      "GET /api/auth/me": signedOut,
      "POST /api/auth/login": () => ({ status: 200, body: alice }),
      "GET /api/tasks": () => ({ status: 200, body: [{ id: "t1", title: "Buy milk", done: false }] }),
    };
    render(<App />);

    await userEvent.type(await screen.findByLabelText("Email"), "alice@example.com");
    await userEvent.type(screen.getByLabelText("Password"), "correct horse battery");
    await userEvent.click(screen.getByRole("button", { name: "Sign in" }));

    expect(await screen.findByText("Buy milk")).toBeInTheDocument();
    expect(screen.getByText("alice@example.com")).toBeInTheDocument();
  });

  it("explains a wrong password and stays on the form", async () => {
    routes = {
      "GET /api/auth/me": signedOut,
      "POST /api/auth/login": () => ({ status: 401, body: { detail: "Wrong email or password." } }),
    };
    render(<App />);

    await userEvent.type(await screen.findByLabelText("Email"), "alice@example.com");
    await userEvent.type(screen.getByLabelText("Password"), "not the password");
    await userEvent.click(screen.getByRole("button", { name: "Sign in" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("Wrong email or password.");
    expect(calls).not.toContain("GET /api/tasks");
  });
});

describe("tasks", () => {
  beforeEach(() => {
    routes = {
      "GET /api/auth/me": () => ({ status: 200, body: alice }),
      "GET /api/tasks": () => ({ status: 200, body: [] }),
    };
  });

  it("adds a task", async () => {
    routes["POST /api/tasks"] = (init) => ({
      status: 201,
      body: { id: "t1", title: JSON.parse(String(init?.body)).title, done: false },
    });
    render(<App />);

    await userEvent.type(await screen.findByLabelText("New task"), "  Write the report ");
    await userEvent.click(screen.getByRole("button", { name: "Add task" }));

    expect(await screen.findByText("Write the report")).toBeInTheDocument();
    expect(screen.getByLabelText("New task")).toHaveValue("");
  });

  it("marks a task done", async () => {
    routes["GET /api/tasks"] = () => ({ status: 200, body: [{ id: "t1", title: "Buy milk", done: false }] });
    routes["PATCH /api/tasks/t1"] = () => ({ status: 200, body: { id: "t1", title: "Buy milk", done: true } });
    render(<App />);

    await userEvent.click(await screen.findByRole("checkbox", { name: "Buy milk" }));

    await waitFor(() => expect(screen.getByRole("checkbox", { name: "Buy milk" })).toBeChecked());
  });

  it("deletes a task", async () => {
    routes["GET /api/tasks"] = () => ({ status: 200, body: [{ id: "t1", title: "Buy milk", done: false }] });
    routes["DELETE /api/tasks/t1"] = () => ({ status: 204 });
    render(<App />);

    await userEvent.click(await screen.findByRole("button", { name: "Delete Buy milk" }));

    expect(await screen.findByText("No tasks yet. Add the first one above.")).toBeInTheDocument();
    // The API refuses changes that are not JSON, even without a body.
    expect(contentTypes["DELETE /api/tasks/t1"]).toBe("application/json");
  });

  it("says so when a change does not save", async () => {
    routes["POST /api/tasks"] = () => ({ status: 500 });
    render(<App />);

    await userEvent.type(await screen.findByLabelText("New task"), "Buy milk");
    await userEvent.click(screen.getByRole("button", { name: "Add task" }));

    expect(await screen.findByRole("alert")).toHaveTextContent("That did not save. Try again.");
  });

  it("goes back to sign-in when the session has expired", async () => {
    routes["POST /api/tasks"] = signedOut;
    render(<App />);

    await userEvent.type(await screen.findByLabelText("New task"), "Buy milk");
    await userEvent.click(screen.getByRole("button", { name: "Add task" }));

    expect(await screen.findByRole("heading", { name: "Sign in" })).toBeInTheDocument();
  });

  it("signs out even when the request fails", async () => {
    routes["POST /api/auth/logout"] = () => ({ status: 500 });
    vi.spyOn(console, "error").mockImplementation(() => {});
    render(<App />);

    await userEvent.click(await screen.findByRole("button", { name: "Sign out" }));

    expect(await screen.findByRole("heading", { name: "Sign in" })).toBeInTheDocument();
  });

  it("signs out", async () => {
    routes["POST /api/auth/logout"] = () => ({ status: 204 });
    render(<App />);

    await userEvent.click(await screen.findByRole("button", { name: "Sign out" }));

    expect(await screen.findByRole("heading", { name: "Sign in" })).toBeInTheDocument();
  });
});
