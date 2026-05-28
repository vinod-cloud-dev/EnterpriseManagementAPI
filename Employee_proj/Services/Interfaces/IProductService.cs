using Employee_proj.DTOs.Product;
using Employee_proj.Models;

namespace Employee_proj.Services.Interfaces
{
    public interface IProductService
    {
        Task<Product> CreateAsync(ProductCreateDto dto);
        Task<IEnumerable<Product>> GetPagedAsync(int page, int pageSize);
        Task<Product?> GetByIdAsync(int id);
        Task UpdateAsync(int id, ProductCreateDto dto);
        Task DeleteAsync(int id);
    }
}
