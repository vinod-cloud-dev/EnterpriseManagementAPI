using System.Text.Json;
using Microsoft.Extensions.Caching.Distributed;
using Employee_proj.Services.Interfaces;

namespace Employee_proj.Services.Implementations
{
    public class CacheService : ICacheService
    {
        private readonly IDistributedCache _cache;
        private readonly ILogger<CacheService> _logger;
            
        public CacheService(IDistributedCache cache, ILogger<CacheService> logger)
        {
            _cache = cache;
            _logger = logger;
        }

        public async Task<T?> GetAsync<T>(String key)
        {
            var data = await _cache.GetStringAsync(key);
            if(data == null)
            {
                _logger.LogInformation($"CACHE MISS: {key}");
                return default;
            }
            _logger.LogInformation($"CACHE HIT: {key}");
            return JsonSerializer.Deserialize<T>(data);

        }

        public async Task SetAsync<T>(string key, T value, TimeSpan? expiry = null)
        {
            var options = new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = expiry ?? TimeSpan.FromMinutes(5)
            };

            var jsonData = JsonSerializer.Serialize(value);

            await _cache.SetStringAsync(key, jsonData, options);

            _logger.LogInformation($"CACHE SET: {key}");
        }
        public async Task RemoveAsync(string key)
        {
            await _cache.RemoveAsync(key);
            _logger.LogInformation($"CACHE REMOVED: {key}");
        }
    }
}
