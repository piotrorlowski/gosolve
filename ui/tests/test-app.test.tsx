import React from "react"

import { describe, it, expect, beforeAll, afterEach, afterAll } from "vitest"
import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { http, HttpResponse } from "msw"
import { setupServer } from "msw/node"
import App  from "../src/App"

const server = setupServer(
  http.get("http://localhost:8000/index/:value", ({ params }) => {
    const { value } = params
    if (value === "100") {
      return HttpResponse.json({
        value: 100,
        index: 1,
      })
    }
    return HttpResponse.json({
      error_message: "Index not found.",
    })
  }),
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe("Test App component", () => {
  it("renders the component correctly", () => {
    render(<App />)

    expect(screen.getByText("Number Index Finder")).toBeInTheDocument()
    expect(screen.getByLabelText(/enter a number/i)).toBeInTheDocument()
    expect(screen.getByText("Get Index")).toBeInTheDocument()
  })

  it("only allows numeric input", async () => {
    render(<App />)
    const input = screen.getByLabelText(/enter a number/i)

    await userEvent.type(input, "123")
    expect(input).toHaveValue("123")

    await userEvent.type(input, "abc")
    expect(input).toHaveValue("123")
  })

  it("displays success message when index is found", async () => {
    render(<App />)

    const input = screen.getByLabelText(/enter a number/i)
    await userEvent.type(input, "100")

    const submitButton = screen.getByText("Get Index")
    await userEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/the given value is/i)).toBeInTheDocument()
      expect(screen.getByText("100")).toBeInTheDocument()
      expect(screen.getByText("1")).toBeInTheDocument()
    })
  })

  it("displays error message when index is not found", async () => {
    render(<App />)
  
    const input = screen.getByLabelText(/enter a number/i)
    await userEvent.type(input, "999")
  
    const submitButton = screen.getByText("Get Index")
    await userEvent.click(submitButton)
  
    await waitFor(() => {
      expect(screen.getByText(/index not found/i)).toBeInTheDocument()
    })
  })

  it("handles API errors correctly", async () => {
    server.use(
      http.get("http://localhost:8000/index/:value", () => {
        return new HttpResponse(null, { status: 500 })
      }),
    )
    render(<App />)

    const input = screen.getByLabelText(/enter a number/i)
    await userEvent.type(input, "123")

    const submitButton = screen.getByText("Get Index")
    await userEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/failed to fetch data: request failed with status code 500/i)).toBeInTheDocument()
    })
  })
})
