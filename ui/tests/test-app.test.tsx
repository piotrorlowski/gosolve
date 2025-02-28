import '@testing-library/jest-dom'
import React from 'react'
import { describe, it, expect, beforeAll, afterEach, afterAll } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from '../src/App'

const createTestQueryClient = () =>
    new QueryClient({
        defaultOptions: {
            queries: {
                retry: false,
            },
        },
    })

function renderWithQueryClient(children: React.ReactElement) {
    const testQueryClient = createTestQueryClient()
    return render(
        <QueryClientProvider client={testQueryClient}>
            {children}
        </QueryClientProvider>
    )
}

const server = setupServer(
    http.get('http://localhost:8000/index/:value/', ({ params }) => {
        const { value } = params
        if (value === '100') {
            return HttpResponse.json({
                value: 100,
                index: 1,
            })
        }
        throw new HttpResponse('Index not found.', { status: 404 })
    })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('Test App component', () => {
    it('renders the component correctly', () => {
        renderWithQueryClient(<App />)

        expect(screen.getByText('Number Index Finder')).toBeInTheDocument()
        expect(screen.getByLabelText(/enter a number/i)).toBeInTheDocument()
        expect(screen.getByText('Get index')).toBeInTheDocument()
    })

    it('only allows numeric input', async () => {
        renderWithQueryClient(<App />)
        const input = screen.getByLabelText(/enter a number/i)

        await userEvent.type(input, '123')
        expect(input).toHaveValue(123)

        await userEvent.type(input, 'abc')
        expect(input).toHaveValue(123)
    })

    it('displays success message when index is found', async () => {
        renderWithQueryClient(<App />)

        const input = screen.getByLabelText(/enter a number/i)
        await userEvent.type(input, '100')

        const submitButton = screen.getByText('Get index')
        await userEvent.click(submitButton)

        await waitFor(() => {
            expect(screen.getByText(/the given value is/i)).toBeInTheDocument()
            expect(screen.getByText('100')).toBeInTheDocument()
            expect(screen.getByText('1')).toBeInTheDocument()
        })
    })

    it('displays error message when index is not found', async () => {
        renderWithQueryClient(<App />)

        const input = screen.getByLabelText(/enter a number/i)
        await userEvent.type(input, '999')

        const submitButton = screen.getByText('Get index')
        await userEvent.click(submitButton)

        await waitFor(() => {
            expect(screen.getByText(/index not found/i)).toBeInTheDocument()
        })
    })

    it('handles API errors correctly', async () => {
        server.use(
            http.get('http://localhost:8000/index/:value/', () => {
                throw new HttpResponse('Failed to fetch data:', {
                    status: 500,
                })
            })
        )
        renderWithQueryClient(<App />)

        const input = screen.getByLabelText(/enter a number/i)
        await userEvent.type(input, '123')

        const submitButton = screen.getByText('Get index')
        await userEvent.click(submitButton)

        await waitFor(() => {
            expect(
                screen.getByText(/failed to fetch data/i)
            ).toBeInTheDocument()
        })
    })
})
