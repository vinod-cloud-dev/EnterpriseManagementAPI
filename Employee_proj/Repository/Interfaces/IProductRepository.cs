using Employee_proj.Models;

namespace Employee_proj.Repository.Interfaces
{
    public interface IProductRepository
    {
        Task<IEnumerable<Product>> GetPagedAsync(int page, int pageSize);
        Task<bool> CategoryExistsAsync(int categoryId);
        Task<Product?> GetByIdAsync(int id);
        Task AddAsync(Product product);
        Task UpdateAsync(Product product);
        Task DeleteAsync(int id);
    }
}
