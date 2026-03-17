using Employee_proj.DTOs.Product;
using Employee_proj.Models;
using Employee_proj.Repository.Interfaces;
using Employee_proj.Services.Interfaces;
using Microsoft.Extensions.Caching.Memory;

namespace Employee_proj.Services.Implementations
{
    public class ProductService: IProductService
    {
        private readonly IProductRepository _repo;
        private readonly IWebHostEnvironment _env;
        private readonly IMemoryCache _cache;
        public ProductService(IProductRepository repo, IWebHostEnvironment env, IMemoryCache cache)
        {
            _repo = repo;
            _env = env;
            _cache = cache;
        }

        public async Task<Product> CreateAsync(ProductCreateDto dto)
        {
            string? imagePath = null;

            if (dto.Image != null)
            {
                var folder = Path.Combine(_env.WebRootPath, "images");
                Directory.CreateDirectory(folder);

                var fileName = Guid.NewGuid() + Path.GetExtension(dto.Image.FileName);
                var path = Path.Combine(folder, fileName);

                using var stream = new FileStream(path, FileMode.Create);
                await dto.Image.CopyToAsync(stream);

                imagePath = "/images/" + fileName;
            }

            var product = new Product
            {
                ProductName = dto.ProductName,
                CategoryId = dto.CategoryId,
                Price = dto.Price,
                Description = dto.Description,
                ImageUrl = imagePath
            };
            await _repo.AddAsync(product);
            _cache.Remove("product_list");
            return product;
        }
        public async Task<IEnumerable<Product>> GetAllAsync()
        {
            string cacheKey = "product_list";
            if (!_cache.TryGetValue(cacheKey, out IEnumerable<Product>? products))
            {
                // Not in cache → get from database
                products = await _repo.GetAllAsync();
                // Store in cache for 5 minutes
                _cache.Set(cacheKey, products, TimeSpan.FromMinutes(5));
            }
            return products ?? Enumerable.Empty<Product>();
        }
        public async Task<Product?> GetByIdAsync(int id)
        {
            string cacheKey = $"product_{id}";
            if (!_cache.TryGetValue(cacheKey, out Product? product))
            {
                Console.WriteLine("❌ Data coming from DATABASE");

                product = await _repo.GetByIdAsync(id);
                if (product != null)
                {
                    _cache.Set(cacheKey, product, TimeSpan.FromMinutes(5));
                }
            }
            else
            {
                Console.WriteLine("✅ Data coming from CACHE");
            }
            return product;
        }
        public async Task UpdateAsync(int id, ProductCreateDto dto)
        {
            var product = await _repo.GetByIdAsync(id);
            if (product == null) throw new Exception("Product not found");

            product.ProductName = dto.ProductName;
            product.CategoryId = dto.CategoryId;
            product.Price = dto.Price;
            product.Description = dto.Description;

            if (dto.Image != null)
            {
                var folder = Path.Combine(_env.WebRootPath, "images");
                Directory.CreateDirectory(folder);

                var fileName = Guid.NewGuid() + Path.GetExtension(dto.Image.FileName);
                var path = Path.Combine(folder, fileName);

                using var stream = new FileStream(path, FileMode.Create);
                await dto.Image.CopyToAsync(stream);

                product.ImageUrl = "/images/" + fileName;
            }

            await _repo.UpdateAsync(product);
            _cache.Remove("product_list");
            _cache.Remove($"product_{id}");
        }
        public async Task DeleteAsync(int id)
        {
            await _repo.DeleteAsync(id);
            _cache.Remove("product_list");
            _cache.Remove($"product_{id}");
        }
    }
}
