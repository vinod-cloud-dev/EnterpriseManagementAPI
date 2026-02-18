using Employee_proj.DTOs.Category;
using Employee_proj.Models;

namespace Employee_proj.Services.Interfaces
{
    public interface ICategoryService
    {
        Task<Category> CreateAsync(CategoryCreateDto dto);
        Task<IEnumerable<Category>> GetAllAsync();
        Task<Category?> GetByIdAsync(int id);
        Task UpdateAsync(int id, CategoryCreateDto dto);
        Task DeleteAsync(int id);
    }
}
