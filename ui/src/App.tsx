import axios from 'axios'
import { useMutation } from '@tanstack/react-query'
import { useState } from 'react'
import { ENDPOINTS } from './config'
import { Button, Form, Container, Row, Col, Card, Alert } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

export default function App() {
    const [inputMessage, setInputMessage] = useState<string>('')
    const {
        mutate,
        data: response,
        error,
        isPending: isLoading,
    } = useMutation({
        mutationFn: async () => {
            const res = await axios.post(ENDPOINTS.CHAT(), {
                message: inputMessage,
            })
            return res.data
        },
    })

    return (
        <Container className="py-5">
            <Row className="justify-content-center">
                <Col md={8} lg={6}>
                    <Card className="shadow">
                        <Card.Header className="bg-primary text-white">
                            <h4 className="mb-0">AI Chat</h4>
                        </Card.Header>
                        <Card.Body>
                            <Form
                                onSubmit={(event) => {
                                    event.preventDefault()
                                    mutate()
                                }}
                            >
                                <Form.Group className="mb-3">
                                    <Form.Label htmlFor="chat-input">
                                        Ask a question:
                                    </Form.Label>
                                    <Form.Control
                                        id="chat-input"
                                        type="text"
                                        value={inputMessage}
                                        onChange={(event) =>
                                            setInputMessage(event.target.value)
                                        }
                                        placeholder="Type your question..."
                                    />
                                </Form.Group>

                                <Button
                                    variant="primary"
                                    type="submit"
                                    disabled={!inputMessage || isLoading}
                                    className="w-100"
                                >
                                    {isLoading ? 'Thinking...' : 'Ask AI'}
                                </Button>
                            </Form>

                            {error && (
                                <Alert variant="danger" className="mt-3">
                                    {error.message}
                                </Alert>
                            )}

                            {response && (
                                <Alert variant="primary" className="mt-3">
                                    <p className="mb-0">{response.response}</p>
                                </Alert>
                            )}
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    )
}
