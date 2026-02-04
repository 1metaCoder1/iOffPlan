import React, { useCallback } from 'react'

interface ImageUploadProps {
  images: File[]
  onImagesChange: (images: File[]) => void
  maxImages?: number
  className?: string
}

export function ImageUpload({ 
  images, 
  onImagesChange, 
  maxImages = 3, 
  className = '' 
}: ImageUploadProps) {
  const handleImageUpload = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (!files) return

    const newImages = Array.from(files)
    const totalImages = images.length + newImages.length

    if (totalImages > maxImages) {
      alert(`Максимум ${maxImages} фото`)
      return
    }

    const updatedImages = [...images, ...newImages]
    onImagesChange(updatedImages)
  }, [images, onImagesChange, maxImages])

  const removeImage = useCallback((index: number) => {
    const updatedImages = images.filter((_, i) => i !== index)
    onImagesChange(updatedImages)
  }, [images, onImagesChange])

  return (
    <div className={`space-y-4 ${className}`}>
      <label className="block text-sm font-medium text-bayut-dark mb-2">
        Фотографии недвижимости (до {maxImages} шт.)
      </label>
      
      <div className="grid grid-cols-3 gap-4">
        {images.map((image, index) => (
          <div key={index} className="relative group">
            <div className="aspect-square bg-gray-100 rounded-lg overflow-hidden">
              <img
                src={URL.createObjectURL(image)}
                alt={`Фото ${index + 1}`}
                className="w-full h-full object-cover"
              />
            </div>
            <button
              type="button"
              onClick={() => removeImage(index)}
              className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
            >
              ×
            </button>
            <div className="absolute bottom-2 left-2 bg-black/60 text-white text-xs px-2 py-1 rounded">
              Фото {index + 1}
            </div>
          </div>
        ))}
        
        {images.length < maxImages && (
          <label className="aspect-square border-2 border-dashed border-gray-300 rounded-lg flex flex-col items-center justify-center cursor-pointer hover:border-gray-400 transition-colors">
            <input
              type="file"
              accept="image/*"
              multiple
              onChange={handleImageUpload}
              className="hidden"
            />
            <div className="text-center">
              <svg className="w-8 h-8 text-gray-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              <span className="text-sm text-gray-600">Добавить фото</span>
            </div>
          </label>
        )}
      </div>
      
      <div className="text-xs text-gray-500">
        {images.length} из {maxImages} фото добавлено
      </div>
    </div>
  )
}