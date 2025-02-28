import React from 'react'
import axios from 'axios'
import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { Button, Form, Container, Row, Col, Card, Alert } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

type IndexResponse = {
    value?: number
    index?: number
}

export default function App() {
    const [inputValue, setInputValue] = useState<string>('')
    const {
        mutate,
        data: result,
        error,
    } = useMutation<IndexResponse>({
        mutationFn: async () => {
            try {
                const response = await axios.get(
                    `http://localhost:8000/index/${inputValue}/`
                )
                return response.data
            } catch (err) {
                throw new Error(
                    axios.isAxiosError(err) && err.response?.status === 404
                        ? 'Index not found.'
                        : `Failed to fetch data: ${String(err)}`
                )
            }
        },
    })

    return (
        <Container className="py-5">
            <Row className="justify-content-center">
                <Col md={8} lg={6}>
                    <Card className="shadow">
                        <Card.Header className="bg-primary text-white">
                            <h4 className="mb-0">Number Index Finder</h4>
                        </Card.Header>
                        <Card.Body>
                            <Form
                                onSubmit={(event) => {
                                    event.preventDefault()
                                    mutate()
                                }}
                            >
                                <Form.Group className="mb-3">
                                    <Form.Label htmlFor="number-input">
                                        Enter a number
                                    </Form.Label>
                                    <Form.Control
                                        id="number-input"
                                        type="number"
                                        value={inputValue}
                                        min={0}
                                        onChange={(event) =>
                                            setInputValue(event.target.value)
                                        }
                                        placeholder="Enter number"
                                    />
                                    <Form.Text className="text-muted">
                                        Only numeric values are allowed.
                                    </Form.Text>
                                </Form.Group>

                                <Button
                                    variant="primary"
                                    type="submit"
                                    disabled={!inputValue}
                                    className="w-100"
                                >
                                    Get index
                                </Button>
                            </Form>

                            {error && (
                                <Alert variant="danger" className="mt-3">
                                    {error.message}
                                </Alert>
                            )}

                            {result && (
                                <Alert variant="success" className="mt-3">
                                    <p className="mb-0">
                                        The given value is{' '}
                                        <strong>{result.value}</strong> and the
                                        index for this value is{' '}
                                        <strong>{result.index}</strong>.
                                    </p>
                                </Alert>
                            )}
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    )
}
