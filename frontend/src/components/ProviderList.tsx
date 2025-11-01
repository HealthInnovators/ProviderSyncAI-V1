import type { Provider } from '../types/provider'
import ProviderCard from './ProviderCard'

interface ProviderListProps {
  providers: Provider[]
  isLoading?: boolean
}

export default function ProviderList({ providers, isLoading }: ProviderListProps) {
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-gray-500">Searching providers...</div>
      </div>
    )
  }

  if (providers.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-12 text-center">
        <p className="text-gray-500 text-lg">No providers found</p>
        <p className="text-gray-400 text-sm mt-2">
          Try adjusting your search criteria
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-900">
          Found {providers.length} provider{providers.length !== 1 ? 's' : ''}
        </h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {providers.map((provider) => (
          <ProviderCard key={provider.npi} provider={provider} />
        ))}
      </div>
    </div>
  )
}

