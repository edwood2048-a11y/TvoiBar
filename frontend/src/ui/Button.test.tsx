import { render, screen } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Button } from '../shared/ui/Button'

// Mock the useTelegram hook
vi.mock('../../shared/lib/useTelegram', () => ({
  useTelegram: () => ({
    user: { id: 1, username: 'testuser' }
  })
}))

describe('Button', () => {
  it('renders with text', () => {
    render(<Button>Test Button</Button>)
    expect(screen.getByText('Test Button')).toBeInTheDocument()
  })

  it('handles click', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click Me</Button>)
    const button = screen.getByText('Click Me')
    button.click()
    expect(handleClick).toHaveBeenCalledTimes(1)
  })
})