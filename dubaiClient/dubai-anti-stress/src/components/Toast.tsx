import { useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import type { RootState } from '../store'
import { hideToast } from '../features/uiSlice'

export const Toast = () => {
  const dispatch = useDispatch()
  const { toastMessage, toastType } = useSelector((state: RootState) => state.ui)

  useEffect(() => {
    if (toastMessage) {
      const timer = setTimeout(() => {
        dispatch(hideToast())
      }, 3000)
      return () => clearTimeout(timer)
    }
  }, [toastMessage, dispatch])

  if (!toastMessage) return null

  const bgColor = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    info: 'bg-blue-500'
  }[toastType || 'info']

  return (
    <div className={`fixed bottom-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg animate-fade-in-up`}>
      {toastMessage}
    </div>
  )
}