import { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import type { RootState } from './store'
import type { Property } from './features/propertySlice'
import UnitsPage from './pages/UnitsPage'

function App() {
  const { loading, error } = useSelector((state: RootState) => state.properties)
  //const { user, isAuthenticated } = useSelector((state: RootState) => state.user)
  
  // Пример моковых данных для демонстрации
  const mockProperties: Property[] = [
    {
      id: '1',
      title: 'Luxury Apartment in Downtown Dubai',
      description: 'Beautiful 2-bedroom apartment with stunning views of Burj Khalifa. Perfect location with easy access to all amenities and public transport.',
      propertyType: 'apartment',
      location: 'Downtown Dubai',
      area: 120,
      bedrooms: 2,
      bathrooms: 2,
      price: 1500000,
      amenities: ['Pool', 'Gym', 'Parking', 'Security', 'Balcony', 'Smart Home'],
      images: ['https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'],
      sellerId: 'user1',
      isVerified: true,
      createdAt: new Date().toISOString(),
      noBrokerReason: 'I want to save 5% commission and get a fair price directly to buyer'
    },
    {
      id: '2',
      title: 'Villa in Al Satwa with Garden',
      description: 'Spacious 4-bedroom villa with private garden and pool. Recently renovated with modern finishes and high-quality materials throughout.',
      propertyType: 'villa',
      location: 'Al Satwa',
      area: 350,
      bedrooms: 4,
      bathrooms: 3,
      price: 3200000,
      amenities: ['Pool', 'Garden', 'Garage', 'BBQ Area', 'Smart Home', 'Security System'],
      images: ['https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'],
      sellerId: 'user2',
      isVerified: true,
      createdAt: new Date().toISOString(),
      noBrokerReason: 'Direct sale to avoid broker fees and get faster transaction'
    },
    {
      id: '3',
      title: 'Modern Studio in Business Bay',
      description: 'Contemporary studio apartment with floor-to-ceiling windows offering panoramic views of Dubai skyline. Fully furnished with premium appliances.',
      propertyType: 'apartment',
      location: 'Business Bay',
      area: 45,
      bedrooms: 0,
      bathrooms: 1,
      price: 750000,
      amenities: ['Pool', 'Gym', 'Sauna', 'Concierge', 'Parking', 'Smart Home'],
      images: ['https://images.unsplash.com/photo-1497366754035-f200968a6e72?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'],
      sellerId: 'user3',
      isVerified: true,
      createdAt: new Date().toISOString(),
      noBrokerReason: 'Selling directly to save commission and provide honest pricing'
    }
  ]

  const [activeProperties, setActiveProperties] = useState<Property[]>([])
  const [activeTab, setActiveTab] = useState<'home' | 'units'>('home')

  useEffect(() => {
    // Имитация загрузки данных
    const timer = setTimeout(() => {
      setActiveProperties(mockProperties)
    }, 500)
    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="min-h-screen bg-bayut-light text-bayut-dark">
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur border-b border-bayut-border">
        <div className="container py-3 flex items-center justify-between gap-4">
          <div className="font-bold text-bayut-dark">
            Dubai <span className="text-bayut-secondary">Anti-Stress</span>
          </div>
          <nav className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setActiveTab('home')}
              className={[
                'px-3 py-2 rounded-xl text-sm font-medium transition-colors',
                activeTab === 'home'
                  ? 'bg-blue-50 text-bayut-primary'
                  : 'text-bayut-gray hover:bg-gray-50 hover:text-bayut-dark',
              ].join(' ')}
            >
              Home
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('units')}
              className={[
                'px-3 py-2 rounded-xl text-sm font-medium transition-colors',
                activeTab === 'units'
                  ? 'bg-blue-50 text-bayut-primary'
                  : 'text-bayut-gray hover:bg-gray-50 hover:text-bayut-dark',
              ].join(' ')}
            >
              Objects (Units)
            </button>
          </nav>
        </div>
      </header>

      {activeTab === 'units' ? (
        <UnitsPage />
      ) : (
        <>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-bayut-primary to-blue-700 text-white py-16 md:py-24">
        <div className="container">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-block bg-white/10 backdrop-blur-sm px-4 py-1 rounded-full mb-6">
              <span className="text-sm font-medium">Direct Property Deals</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold mb-6">
              Find Real Estate Deals <span className="text-bayut-secondary">Without Broker Stress</span>
            </h1>
            <p className="text-xl text-blue-100 mb-10">
              Connect directly with property owners and save thousands in broker commissions. No hidden fees, no middlemen.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="btn btn-secondary px-8 py-4 text-lg font-semibold hover:bg-orange-700">
                <span className="flex items-center justify-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clipRule="evenodd" />
                  </svg>
                  Browse Properties
                </span>
              </button>
              <button className="btn btn-outline px-8 py-4 text-lg font-semibold text-white border-white hover:bg-white hover:text-bayut-primary">
                <span className="flex items-center justify-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-7V7a1 1 0 10-2 0v4a1 1 0 102 0zm-1 4a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
                  </svg>
                  List Your Property
                </span>
              </button>
            </div>
            
            <div className="mt-12 flex flex-wrap justify-center gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold mb-2">5%</div>
                <div className="text-blue-200">Average Broker Commission Saved</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold mb-2">24/7</div>
                <div className="text-blue-200">Direct Owner Communication</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold mb-2">100%</div>
                <div className="text-blue-200">Verified Listings</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="section-title">Why Choose Direct Deals?</h2>
            <p className="section-subtitle mx-auto">
              Our platform eliminates broker commissions while providing full transparency and security for both buyers and sellers.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="card p-8 text-center">
              <div className="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-bayut-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 16V7a2 2 0 00-2-2H9a2 2 0 00-2 2v9m7-10h2a2 2 0 012 2v9m-7 0a2 2 0 01-2-2v-9" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-bayut-dark">Save 5% Commission</h3>
              <p className="text-bayut-gray">
                Typical broker fees for primary sales in Dubai range from 4-6%. We help you keep that money in your pocket.
              </p>
            </div>
            
            <div className="card p-8 text-center">
              <div className="w-16 h-16 bg-orange-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-bayut-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9s1.532 4.762 6 6.216a12.02 12.02 0 006.784 1.538 11.955 11.955 0 01-6.784 1.538 12.02 12.02 0 006-6.216s1.532-5.046-.79-7.016a12.02 12.02 0 00-6.692-2.016zm0 1.016a11 11 0 00-9 5.016 11 11 0 009 5.016 11 11 0 009-5.016 11 11 0 00-9-5.016z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-bayut-dark">Direct Communication</h3>
              <p className="text-bayut-gray">
                Chat directly with property owners without broker interference. Get honest answers and negotiate fair prices.
              </p>
            </div>
            
            <div className="card p-8 text-center">
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold mb-3 text-bayut-dark">Verified Owners</h3>
              <p className="text-bayut-gray">
                Every seller undergoes identity verification and property ownership checks to ensure authentic listings.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Properties Section */}
      <section className="py-16 bg-bayut-light">
        <div className="container">
          <div className="text-center mb-12">
            <div className="inline-block bg-blue-50 px-4 py-1 rounded-full mb-4">
              <span className="text-bayut-primary font-medium">Featured Properties</span>
            </div>
            <h2 className="section-title">Latest Direct Listings</h2>
            <p className="section-subtitle mx-auto">
              Discover properties listed directly by owners with no broker markup
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {loading ? (
              <div className="col-span-full flex justify-center py-16">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-bayut-primary"></div>
              </div>
            ) : error ? (
              <div className="col-span-full bg-red-50 text-red-700 p-6 rounded-xl text-center">
                <p className="font-medium">{error}</p>
              </div>
            ) : (
              activeProperties.map((property) => (
                <div key={property.id} className="card group">
                  <div className="relative overflow-hidden h-56">
                    <img 
                      src={property.images[0]} 
                      alt={property.title} 
                      className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
                    
                    <div className="absolute top-4 right-4 flex flex-col gap-2">
                      {property.isVerified && (
                        <span className="badge badge-success flex items-center gap-1">
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                          </svg>
                          Verified Owner
                        </span>
                      )}
                      <span className="badge badge-primary flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-14a1 1 0 10-2 0v1.027a4.558 4.558 0 00-1.25.324 3.703 3.703 0 00-2.098 2.097A4.558 4.558 0 004.973 9H6a1 1 0 100-2H4.973a6.56 6.56 0 011.281-2.564 5.703 5.703 0 013.78-1.409 5.703 5.703 0 013.78 1.409 6.56 6.56 0 011.28 2.564H16a1 1 0 100 2h-1.027a4.558 4.558 0 00-.324 1.25 3.703 3.703 0 002.097 2.098A4.558 4.558 0 0017 11.027V10a1 1 0 10-2 0v1.027a2.558 2.558 0 01-.324 1.25 1.703 1.703 0 01-2.098 2.097A2.558 2.558 0 0111.027 15H10a1 1 0 100 2h1.027a4.558 4.558 0 001.25.324 3.703 3.703 0 002.097-2.098A4.558 4.558 0 0015 13.973V15a1 1 0 102 0v-1.027a6.56 6.56 0 011.281 2.564 5.703 5.703 0 01-1.409 3.78 5.703 5.703 0 01-3.78 1.409A6.56 6.56 0 019 20.973V20a1 1 0 10-2 0v.973a6.56 6.56 0 01-2.564-1.28 5.703 5.703 0 01-1.409-3.78 5.703 5.703 0 011.409-3.78A6.56 6.56 0 016.027 9H5a1 1 0 000 2h1.027a4.558 4.558 0 001.25-.324 1.703 1.703 0 012.097-2.098A2.558 2.558 0 0111 11.027V10a1 1 0 10-2 0v1.027a4.558 4.558 0 01-.324-1.25A3.703 3.703 0 016.579 7.68a4.558 4.558 0 01-1.25-.324H4a1 1 0 100 2h1.027a6.56 6.56 0 002.564 1.28 5.703 5.703 0 003.78 1.409 5.703 5.703 0 003.78-1.409A6.56 6.56 0 0016.43 9.36L16 10a1 1 0 102 0l.43-.94A8.002 8.002 0 0010 2z" clipRule="evenodd" />
                        </svg>
                        No Broker
                      </span>
                    </div>
                  </div>
                  
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="text-xl font-bold text-bayut-dark line-clamp-1">{property.title}</h3>
                        <p className="text-bayut-gray mt-1 text-sm">{property.location}</p>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-bayut-primary">AED {property.price.toLocaleString()}</div>
                        <div className="text-sm text-green-600 font-medium mt-1">
                          Save ~AED {(property.price * 0.05).toLocaleString()}
                        </div>
                      </div>
                    </div>
                    
                    <p className="text-bayut-gray mb-5 line-clamp-2">
                      {property.description}
                    </p>
                    
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
                      <div className="text-center">
                        <div className="font-bold text-bayut-dark">{property.area} sqm</div>
                        <div className="text-xs text-bayut-gray">Area</div>
                      </div>
                      <div className="text-center">
                        <div className="font-bold text-bayut-dark">{property.bedrooms} Bed</div>
                        <div className="text-xs text-bayut-gray">Bedrooms</div>
                      </div>
                      <div className="text-center">
                        <div className="font-bold text-bayut-dark">{property.bathrooms} Bath</div>
                        <div className="text-xs text-bayut-gray">Bathrooms</div>
                      </div>
                      <div className="text-center">
                        <div className="font-bold text-bayut-dark capitalize">{property.propertyType}</div>
                        <div className="text-xs text-bayut-gray">Type</div>
                      </div>
                    </div>
                    
                    <div className="flex gap-3 mb-4">
                      {property.amenities.slice(0, 3).map((amenity, index) => (
                        <span key={index} className="text-xs bg-blue-50 text-bayut-primary px-2.5 py-1 rounded-full">
                          {amenity}
                        </span>
                      ))}
                      {property.amenities.length > 3 && (
                        <span className="text-xs bg-gray-100 text-bayut-gray px-2.5 py-1 rounded-full">
                          +{property.amenities.length - 3} more
                        </span>
                      )}
                    </div>
                    
                    <button className="btn btn-primary w-full font-medium py-3">
                      <span className="flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-2 0c0 .993-.241 1.929-.668 2.754l-1.524-1.525a3.997 3.997 0 00.078-2.183l1.526-1.526A5.998 5.998 0 0016 10zm-4.5 1.127a1.998 1.998 0 00-.123-1.132l1.525-1.525a3.997 3.997 0 00-2.183.078l-1.525 1.524a1.997 1.997 0 001.132-.123zm-1.45 1.45l1.525-1.525a1.997 1.997 0 00-.123-1.132 1.998 1.998 0 00-1.132.123L9.828 11.47a1.997 1.997 0 00.123 1.132 1.998 1.998 0 001.132-.123zm-1.45-1.45l1.525-1.526a3.997 3.997 0 00-.078-2.183l-1.525 1.526a1.998 1.998 0 00.123 1.132 1.997 1.997 0 001.132.123 1.998 1.998 0 00.123-1.132l-1.526 1.525a3.997 3.997 0 002.183-.078z" clipRule="evenodd" />
                        </svg>
                        Contact Owner
                      </span>
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
          
          <div className="text-center mt-12">
            <button className="btn btn-outline px-8 py-3 font-medium">
              View All Properties
            </button>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-bayut-primary to-blue-700 text-white">
        <div className="container">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Ready to Save on Your Dubai Property Deal?
            </h2>
            <p className="text-xl text-blue-100 mb-10">
              Join thousands of satisfied users who have saved thousands in broker commissions by dealing directly with property owners.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="btn btn-secondary px-8 py-4 text-lg font-semibold">
                Get Started Now
              </button>
              <button className="btn btn-outline px-8 py-4 text-lg font-semibold text-white border-white">
                How It Works
              </button>
            </div>
          </div>
        </div>
      </section>

      <footer className="bg-bayut-dark text-white py-16">
        <div className="container">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-2xl font-bold mb-6">Dubai <span className="text-bayut-secondary">Anti-Stress</span> Deals</h3>
              <p className="text-gray-400 mb-6">
                The first platform in Dubai for direct property transactions without broker commissions. Save money, time, and stress.
              </p>
              <div className="flex gap-4">
                <a href="#" className="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-bayut-primary transition-colors">
                  <span className="sr-only">Facebook</span>
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 4.023 9.106 9.106 9.939V15.065H8.434V12h2.672V9.892c0-2.646 1.585-4.095 3.96-4.095 1.14 0 2.336.205 2.336.205v2.568h-1.315c-1.293 0-1.689.804-1.689 1.64V12h2.853l-.454 2.865h-2.399V21.94A10.006 10.006 0 0022 12z" clipRule="evenodd" />
                  </svg>
                </a>
                <a href="#" className="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-bayut-primary transition-colors">
                  <span className="sr-only">Twitter</span>
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                  </svg>
                </a>
                <a href="#" className="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center hover:bg-bayut-primary transition-colors">
                  <span className="sr-only">Instagram</span>
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                    <path fillRule="evenodd" d="M12.315 2c2.43 0 2.786.013 3.808.06 1.064.049 1.791.218 2.427.465a4.902 4.902 0 011.772 1.153 4.902 4.902 0 011.153 1.772c.247.636.416 1.363.465 2.427.048 1.067.06 1.407.06 4.123v.08c0 2.643-.012 2.987-.06 4.043-.049 1.064-.218 1.791-.465 2.427a4.902 4.902 0 01-1.153 1.772 4.902 4.902 0 01-1.772 1.153c-.636.247-1.363.416-2.427.465-1.067.048-1.407.06-4.123.06h-.08c-2.643 0-2.987-.012-4.043-.06-1.064-.049-1.791-.218-2.427-.465a4.902 4.902 0 01-1.772-1.153 4.902 4.902 0 01-1.153-1.772c-.247-.636-.416-1.363-.465-2.427-.047-1.024-.06-1.379-.06-3.808v-.63c0-2.43.013-2.786.06-3.808.049-1.064.218-1.791.465-2.427a4.902 4.902 0 011.153-1.772A4.902 4.902 0 015.45 2.525c.636-.247 1.363-.416 2.427-.465C8.901 2.013 9.256 2 11.685 2h.63zm-.081 1.802h-.468c-2.456 0-2.784.011-3.807.058-.975.045-1.504.207-1.857.344-.467.182-.8.398-1.15.748-.35.35-.566.683-.748 1.15-.137.353-.3.882-.344 1.857-.047 1.023-.058 1.351-.058 3.807v.468c0 2.456.011 2.784.058 3.807.045.975.207 1.504.344 1.857.182.466.399.8.748 1.15.35.35.683.566 1.15.748.353.137.882.3 1.857.344 1.054.048 1.37.058 4.041.058h.08c2.597 0 2.917-.01 3.96-.058.976-.045 1.505-.207 1.858-.344.466-.182.8-.398 1.15-.748.35-.35.566-.683.748-1.15.137-.353.3-.882.344-1.857.048-1.055.058-1.37.058-4.041v-.08c0-2.597-.01-2.917-.058-3.96-.045-.976-.207-1.505-.344-1.858a3.097 3.097 0 00-.748-1.15 3.098 3.098 0 00-1.15-.748c-.353-.137-.882-.3-1.857-.344-1.023-.047-1.351-.058-3.807-.058zM12 6.865a5.135 5.135 0 110 10.27 5.135 5.135 0 010-10.27zm0 1.802a3.333 3.333 0 100 6.666 3.333 3.333 0 000-6.666zm5.338-3.205a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4z" clipRule="evenodd" />
                  </svg>
                </a>
              </div>
            </div>
            <div>
              <h4 className="font-bold text-lg mb-6">Quick Links</h4>
              <ul className="space-y-3">
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Browse Properties</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">List Your Property</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">How It Works</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Pricing</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Blog & Resources</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-lg mb-6">Legal</h4>
              <ul className="space-y-3">
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Terms of Service</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Cookie Policy</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">FAQ</a></li>
                <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Contact Us</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold text-lg mb-6">Contact</h4>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-bayut-secondary flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span className="text-gray-400">Dubai, UAE<br/>Business Bay, Level 12</span>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-bayut-secondary flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  <span className="text-gray-400">+971 4 XXX XXXX<br/>support@dubaideals.com</span>
                </li>
                <li className="flex items-start gap-3">
                  <svg className="w-5 h-5 text-bayut-secondary flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="text-gray-400">Mon-Fri: 9AM - 6PM<br/>Sat: 10AM - 2PM</span>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-gray-500">
            © {new Date().getFullYear()} Dubai Anti-Stress Deals. All rights reserved.
          </div>
        </div>
      </footer>
        </>
      )}
    </div>
  )
}

export default App