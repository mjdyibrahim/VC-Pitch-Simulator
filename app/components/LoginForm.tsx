import { useState } from 'react'
import { signIn } from '../auth'

export function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const { data, error } = await signIn(email, password)
    if (error) {
      console.error('Error signing in:', error.message)
    } else {
      console.log('Signed in successfully:', data)
      // Handle successful login (e.g., redirect to dashboard)
    }
  }

  // Render form...
}