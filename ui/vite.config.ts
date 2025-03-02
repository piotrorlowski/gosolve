import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    envDir: '../',
    test: {
        globals: true,
        environment: 'jsdom',
        setupFiles: 'jest.setup.ts',
        css: true,
    },
})
