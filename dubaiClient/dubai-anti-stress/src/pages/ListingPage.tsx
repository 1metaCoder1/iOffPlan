import { useState } from 'react'
import type { ListingFormData, AreaOption, PropertyTypeOption, PropertySubTypeOption, LandTypeOption, ProjectOption } from '../types/listing'
import { ImageUpload } from '../components/ImageUpload'

const MOCK_AREAS: AreaOption[] = [
  { area_id: 1, area_name_en: 'Downtown Dubai' },
  { area_id: 2, area_name_en: 'Business Bay' },
  { area_id: 3, area_name_en: 'Jumeirah Village Circle' },
  { area_id: 4, area_name_en: 'Dubai Marina' },
  { area_id: 5, area_name_en: 'Al Satwa' },
  { area_id: 6, area_name_en: 'Palm Jumeirah' },
  { area_id: 7, area_name_en: 'Arabian Ranches' },
  { area_id: 8, area_name_en: 'Jumeirah Lakes Towers' },
]

const MOCK_PROPERTY_TYPES: PropertyTypeOption[] = [
  { property_type_id: 1, property_type_en: 'Apartment' },
  { property_type_id: 2, property_type_en: 'Villa' },
  { property_type_id: 3, property_type_en: 'Townhouse' },
  { property_type_id: 4, property_type_en: 'Penthouse' },
  { property_type_id: 5, property_type_en: 'Studio' },
]

const MOCK_PROPERTY_SUB_TYPES: PropertySubTypeOption[] = [
  { property_sub_type_id: 1, property_sub_type_en: '1 Bedroom' },
  { property_sub_type_id: 2, property_sub_type_en: '2 Bedrooms' },
  { property_sub_type_id: 3, property_sub_type_en: '3 Bedrooms' },
  { property_sub_type_id: 4, property_sub_type_en: '4 Bedrooms' },
  { property_sub_type_id: 5, property_sub_type_en: '5+ Bedrooms' },
  { property_sub_type_id: 6, property_sub_type_en: 'Duplex' },
  { property_sub_type_id: 7, property_sub_type_en: 'Triplex' },
]

const MOCK_LAND_TYPES: LandTypeOption[] = [
  { land_type_id: 1, land_type_en: 'Residential' },
  { land_type_id: 2, land_type_en: 'Commercial' },
  { land_type_id: 3, land_type_en: 'Mixed Use' },
  { land_type_id: 4, land_type_en: 'Industrial' },
]

const MOCK_PROJECTS: ProjectOption[] = [
  { project_id: 1, project_name_en: 'Burj Views', master_project_id: 1, master_project_en: 'Emaar Downtown' },
  { project_id: 2, project_name_en: 'The Bay Gate', master_project_id: 2, master_project_en: 'Business Bay District' },
  { project_id: 3, project_name_en: 'Bloom Towers', master_project_id: 3, master_project_en: 'Jumeirah Village Circle' },
  { project_id: 4, project_name_en: 'Marina Gate', master_project_id: 4, master_project_en: 'Dubai Marina' },
  { project_id: 5, project_name_en: 'Satwa Villas', master_project_id: 5, master_project_en: 'Al Satwa' },
]

function formatAed(value?: number) {
  if (value == null || Number.isNaN(value)) return '—'
  return new Intl.NumberFormat('en-AE', {
    style: 'currency',
    currency: 'AED',
    maximumFractionDigits: 0,
  }).format(value)
}

function formatArea(value?: number) {
  if (value == null || Number.isNaN(value)) return '—'
  return `${value.toLocaleString()} sqm`
}

function getRoomsLabel(rooms?: number) {
  if (rooms == null) return '—'
  if (rooms === 0) return 'Studio'
  if (rooms === 1) return '1 Bed'
  return `${rooms} Beds`
}

export default function ListingPage() {
  const [formData, setFormData] = useState<ListingFormData>({
    property_type_id: 1,
    property_type_en: 'Apartment',
    property_sub_type_id: 1,
    property_sub_type_en: 'Studio',
    area_id: 1,
    area_name_en: 'Downtown Dubai',
    actual_area: 0,
    rooms: 0,
    rooms_en: 'Studio',
    is_free_hold: 1,
    is_lease_hold: 0,
    is_registered: 1,
    land_type_id: 1,
    land_type_en: 'Residential',
    listing_status: 'draft',
    images: [],
    description: '',
  })

  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleImageChange = (images: File[]) => {
    handleInputChange('images', images)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    // Validate form
    if (formData.actual_area <= 0) {
      alert('Пожалуйста, укажите площадь недвижимости')
      setIsSubmitting(false)
      return
    }

    if (formData.images.length === 0) {
      alert('Пожалуйста, добавьте хотя бы одно фото')
      setIsSubmitting(false)
      return
    }

    // Log form data to console
    console.log('Listing Form Data:', {
      ...formData,
      images: formData.images.map((img, index) => ({
        name: img.name,
        size: img.size,
        type: img.type,
      })),
    });

    alert('Данные формы успешно отправлены! Проверьте консоль для деталей.')
    setIsSubmitting(false)
  }

  return (
    <div className="py-10">
      <div className="container">
        <div className="mb-8">
          <div className="inline-block bg-blue-50 px-4 py-1 rounded-full mb-4">
            <span className="text-bayut-primary font-medium">Objects / Submit Listing</span>
          </div>
          <div className="flex items-center gap-4">
            <button 
              type="button" 
              className="btn btn-outline"
              onClick={() => window.location.href = '/units'}
            >
              <span className="text-sm">← Back to Units</span>
            </button>
            <h2 className="section-title">Submit Property Listing</h2>
          </div>
          <p className="section-subtitle">
            Заполните форму ниже, чтобы разместить ваше объявление о продаже недвижимости в Дубае.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="card p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Property Type</label>
                <select
                  className="form-control"
                  value={formData.property_type_id}
                  onChange={(e) => handleInputChange('property_type_id', Number(e.target.value))}
                >
                  <option value="">Select property type</option>
                  {MOCK_PROPERTY_TYPES.map(pt => (
                    <option key={pt.property_type_id} value={pt.property_type_id}>
                      {pt.property_type_en}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Property Sub-Type</label>
                <select
                  className="form-control"
                  value={formData.property_sub_type_id}
                  onChange={(e) => handleInputChange('property_sub_type_id', Number(e.target.value))}
                >
                  <option value="">Select property sub-type</option>
                  {MOCK_PROPERTY_SUB_TYPES.map(pst => (
                    <option key={pst.property_sub_type_id} value={pst.property_sub_type_id}>
                      {pst.property_sub_type_en}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Area</label>
                <select
                  className="form-control"
                  value={formData.area_id}
                  onChange={(e) => {
                    const selectedArea = MOCK_AREAS.find(a => a.area_id === Number(e.target.value))
                    if (selectedArea) {
                      handleInputChange('area_id', Number(e.target.value))
                      handleInputChange('area_name_en', selectedArea.area_name_en)
                    }
                  }}
                >
                  <option value="">Select area</option>
                  {MOCK_AREAS.map(area => (
                    <option key={area.area_id} value={area.area_id}>
                      {area.area_name_en}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Land Type</label>
                <select
                  className="form-control"
                  value={formData.land_type_id}
                  onChange={(e) => {
                    const selectedLandType = MOCK_LAND_TYPES.find(lt => lt.land_type_id === Number(e.target.value))
                    if (selectedLandType) {
                      handleInputChange('land_type_id', Number(e.target.value))
                      handleInputChange('land_type_en', selectedLandType.land_type_en)
                    }
                  }}
                >
                  <option value="">Select land type</option>
                  {MOCK_LAND_TYPES.map(lt => (
                    <option key={lt.land_type_id} value={lt.land_type_id}>
                      {lt.land_type_en}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Project</label>
                <select
                  className="form-control"
                  value={formData.project_id || '0'}
                  onChange={(e) => {
                    const selectedProject = MOCK_PROJECTS.find(p => p.project_id === Number(e.target.value))
                    if (selectedProject) {
                      handleInputChange('project_id', Number(e.target.value))
                      handleInputChange('project_name_en', selectedProject.project_name_en)
                      handleInputChange('master_project_id', selectedProject.master_project_id)
                      handleInputChange('master_project_en', selectedProject.master_project_en)
                    }
                  }}
                >
                  <option value="">Select project</option>
                  {MOCK_PROJECTS.map(p => (
                    <option key={p.project_id} value={p.project_id}>
                      {p.project_name_en}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Asking Price (AED)</label>
                <input
                  type="number"
                  className="form-control"
                  placeholder="e.g. 1200000"
                  value={formData.asking_price || ''}
                  onChange={(e) => handleInputChange('asking_price', Number(e.target.value))}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Price per sqm (AED)</label>
                <input
                  type="number"
                  className="form-control"
                  placeholder="e.g. 1200"
                  value={formData.price_per_sqm || ''}
                  onChange={(e) => handleInputChange('price_per_sqm', Number(e.target.value))}
                />
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Actual Area (sqm)</label>
                <input
                  type="number"
                  className="form-control"
                  placeholder="e.g. 85"
                  value={formData.actual_area}
                  onChange={(e) => handleInputChange('actual_area', Number(e.target.value))}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Balcony Area (sqm)</label>
                <input
                  type="number"
                  className="form-control"
                  placeholder="e.g. 12"
                  value={formData.unit_balcony_area || ''}
                  onChange={(e) => handleInputChange('unit_balcony_area', Number(e.target.value))}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Rooms</label>
                <input
                  type="number"
                  className="form-control"
                  placeholder="e.g. 2"
                  value={formData.rooms}
                  onChange={(e) => {
                    const rooms = Number(e.target.value)
                    handleInputChange('rooms', rooms)
                    handleInputChange('rooms_en', getRoomsLabel(rooms))
                  }}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Floor</label>
                <input
                  type="text"
                  className="form-control"
                  placeholder="e.g. 12"
                  value={formData.floor || ''}
                  onChange={(e) => handleInputChange('floor', e.target.value)}
                />
              </div>

              <div>
                <div className="flex items-center gap-2">
                  <label className="text-sm font-medium text-bayut-dark">Ownership Type</label>
                  <div className="flex gap-2">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name="ownership"
                        value="freehold"
                        checked={formData.is_free_hold === 1}
                        onChange={() => {
                          handleInputChange('is_free_hold', 1)
                          handleInputChange('is_lease_hold', 0)
                        }}
                      />
                      <span className="ml-2 text-sm">Freehold</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="radio"
                        name="ownership"
                        value="leasehold"
                        checked={formData.is_lease_hold === 1}
                        onChange={() => {
                          handleInputChange('is_free_hold', 0)
                          handleInputChange('is_lease_hold', 1)
                        }}
                      />
                      <span className="ml-2 text-sm">Leasehold</span>
                    </label>
                  </div>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium text-bayut-dark">Registered</label>
                <select
                  className="form-control"
                  value={formData.is_registered}
                  onChange={(e) => handleInputChange('is_registered', Number(e.target.value))}
                >
                  <option value="1">Yes</option>
                  <option value="0">No</option>
                </select>
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Property Description</label>
                <textarea
                  className="form-control h-32"
                  placeholder="Describe your property in detail..."
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                />
              </div>

              <div>
                <ImageUpload
                  images={formData.images}
                  onImagesChange={handleImageChange}
                  maxImages={3}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-bayut-dark mb-2">Contact Information</label>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Contact Person"
                      value={formData.contact_person || ''}
                      onChange={(e) => handleInputChange('contact_person', e.target.value)}
                    />
                  </div>
                  <div>
                    <input
                      type="tel"
                      className="form-control"
                      placeholder="Phone Number"
                      value={formData.contact_phone || ''}
                      onChange={(e) => handleInputChange('contact_phone', e.target.value)}
                    />
                  </div>
                  <div>
                    <input
                      type="email"
                      className="form-control"
                      placeholder="Email Address"
                      value={formData.contact_email || ''}
                      onChange={(e) => handleInputChange('contact_email', e.target.value)}
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="card p-6">
            <div className="flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
              <div className="text-sm text-bayut-gray">
                Please review all information before submitting
              </div>
              <div className="flex gap-3">
                <button
                  type="button"
                  className="btn btn-outline"
                  onClick={() => {
                    setFormData({
                      property_type_id: 1,
                      property_type_en: 'Apartment',
                      property_sub_type_id: 1,
                      property_sub_type_en: 'Studio',
                      area_id: 1,
                      area_name_en: 'Downtown Dubai',
                      actual_area: 0,
                      rooms: 0,
                      rooms_en: 'Studio',
                      is_free_hold: 1,
                      is_lease_hold: 0,
                      is_registered: 1,
                      land_type_id: 1,
                      land_type_en: 'Residential',
                      listing_status: 'draft',
                      images: [],
                      description: '',
                    })
                  }}
                >
                  Reset Form
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="btn btn-primary">
                  {isSubmitting ? 'Submitting...' : 'Submit Listing'}
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}