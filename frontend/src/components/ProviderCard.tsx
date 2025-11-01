import type { Provider } from '../types/provider'

interface ProviderCardProps {
  provider: Provider
}

export default function ProviderCard({ provider }: ProviderCardProps) {
  const displayName = provider.first_name && provider.last_name
    ? `${provider.first_name} ${provider.last_name}`
    : provider.organization_name || 'Unknown Provider'

  const location = [provider.city, provider.state, provider.postal_code]
    .filter(Boolean)
    .join(', ')

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-lg font-semibold text-gray-900">{displayName}</h3>
        <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
          {provider.enumeration_type}
        </span>
      </div>
      
      <div className="space-y-1 text-sm text-gray-600">
        <div>
          <span className="font-medium">NPI:</span> {provider.npi}
        </div>
        {location && (
          <div>
            <span className="font-medium">Location:</span> {location}
          </div>
        )}
        {provider.taxonomy && (
          <div>
            <span className="font-medium">Specialty:</span> {provider.taxonomy}
          </div>
        )}
      </div>

      {provider.website && (
        <div className="mt-3">
          <a
            href={provider.website}
            target="_blank"
            rel="noreferrer"
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            Visit Website →
          </a>
        </div>
      )}
    </div>
  )
}

