import { useState } from 'react'
import type { ProviderSearchRequest } from '../types/provider'

interface SearchBarProps {
  onSearch: (params: ProviderSearchRequest) => void
  isLoading?: boolean
}

export default function SearchBar({ onSearch, isLoading }: SearchBarProps) {
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [organizationName, setOrganizationName] = useState('')
  const [city, setCity] = useState('')
  const [state, setState] = useState('')
  const [postalCode, setPostalCode] = useState('')
  const [taxonomy, setTaxonomy] = useState('')

  const handleSearch = () => {
    const params: ProviderSearchRequest = {}
    if (firstName) params.first_name = firstName
    if (lastName) params.last_name = lastName
    if (organizationName) params.organization_name = organizationName
    if (city) params.city = city
    if (state) params.state = state
    if (postalCode) params.postal_code = postalCode
    if (taxonomy) params.taxonomy = taxonomy
    params.limit = 10
    
    onSearch(params)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 className="text-lg font-semibold mb-4">Search Providers</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <input
          className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <input
          className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Last Name"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <input
          className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Organization Name"
          value={organizationName}
          onChange={(e) => setOrganizationName(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <input
          className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="City"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <input
          className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="State"
          value={state}
          onChange={(e) => setState(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <input
          className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Postal Code"
          value={postalCode}
          onChange={(e) => setPostalCode(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <input
          className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Taxonomy/Specialty"
          value={taxonomy}
          onChange={(e) => setTaxonomy(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button
          className="bg-blue-600 text-white rounded-md px-4 py-2 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          onClick={handleSearch}
          disabled={isLoading}
        >
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </div>
    </div>
  )
}

