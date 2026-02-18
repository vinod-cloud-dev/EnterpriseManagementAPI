using Employee_proj.DTOs.Product;
using Employee_proj.Models;
using Employee_proj.Repository.Interfaces;
using Employee_proj.Services.Interfaces;

namespace Employee_proj.Services.Implementations
{
    public class ProductService: IProductService
    {
        private readonly IProductRepository _repo;
        private readonly IWebHostEnvironment _env;

        public ProductService(IProductRepository repo, IWebHostEnvironment env)
        {
            _repo = repo;
            _env = env;
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
            return product;
        }

        public async Task<IEnumerable<Product>> GetAllAsync()
        {
            return await _repo.GetAllAsync();
        }

        public async Task<Product?> GetByIdAsync(int id)
        {
            return await _repo.GetByIdAsync(id);
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
        }

        public async Task DeleteAsync(int id)
        {
            await _repo.DeleteAsync(id);
        }
    }
}
