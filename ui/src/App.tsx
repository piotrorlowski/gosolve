import React from "react"

import axios from "axios"
import { useState } from "react"
import { Button, Form, Container, Row, Col, Card, Alert } from "react-bootstrap"
import "bootstrap/dist/css/bootstrap.min.css"

interface IndexResponse {
  value?: number
  index?: number
  error_message?: string
}

export default function App() {
  const [inputValue, setInputValue] = useState<string>("")
  const [result, setResult] = useState<IndexResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Only allow numeric input
    const value = e.target.value
    if (value === "" || /^\d+$/.test(value)) {
      setInputValue(value)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    setError(null)

    try {
      const response = await axios.get(`http://localhost:8000/index/${inputValue}/`)
      setResult(response.data)
    } catch (err) {
      setError(`Failed to fetch data: ${axios.isAxiosError(err) ? err.message : String(err)}`)
      setResult(null)
    }
  }

  return (
    <Container className="py-5">
      <Row className="justify-content-center">
        <Col md={8} lg={6}>
          <Card className="shadow">
            <Card.Header className="bg-primary text-white">
              <h4 className="mb-0">Number Index Finder</h4>
            </Card.Header>
            <Card.Body>
            <Form onSubmit={handleSubmit}>
              <Form.Group className="mb-3">
                <Form.Label htmlFor="number-input">Enter a number</Form.Label>
                <Form.Control
                  id="number-input"
                  type="text"
                  value={inputValue}
                  onChange={handleInputChange}
                  placeholder="Enter number"
                />
                <Form.Text className="text-muted">Only numeric values are allowed.</Form.Text>
              </Form.Group>

              <Button variant="primary" type="submit" disabled={!inputValue} className="w-100">
                  Get Index
              </Button>
            </Form>

            {error && (
              <Alert variant="danger" className="mt-3">
                {error}
              </Alert>
            )}

            {result && (
              <Alert variant={result.error_message ? "warning" : "success"} className="mt-3">
                {result.error_message ? (
                  <p className="mb-0">{result.error_message}</p>
                ) : (
                  <p className="mb-0">
                    The given value is <strong>{result.value}</strong> and the 
                    index for this value is <strong>{result.index}</strong>.
                  </p>
                )}
              </Alert>
            )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}
