import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'
import { getCurrentUser } from '../auth'

export function ProtectedRoute({ children }) {
  const router = useRouter()
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    const checkAuth = async () => {
      const { data: { user } } = await getCurrentUser()
      if (user) {
        setIsAuthenticated(true)
      } else {
        router.push('/login')
      }
    }
    checkAuth()
  }, [router])

  if (!isAuthenticated) {
    return null // or a loading spinner
  }

  return children
}