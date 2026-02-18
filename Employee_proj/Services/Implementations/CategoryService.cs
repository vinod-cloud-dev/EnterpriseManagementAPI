using Employee_proj.DTOs.Category;
using Employee_proj.Models;
using Employee_proj.Repository.Interfaces;
using Employee_proj.Services.Interfaces;

namespace Employee_proj.Services.Implementations
{
    public class CategoryService : ICategoryService
    {
        private readonly ICategoryRepository _repo;

        public CategoryService(ICategoryRepository repo)
        {
            _repo = repo;
        }

        public async Task<Category> CreateAsync(CategoryCreateDto dto)
        {
            var category = new Category
            {
                CategoryName = dto.CategoryName,
                CategoryDescription = dto.CategoryDescription
            };

            await _repo.AddAsync(category);
            return category;
        }

        public async Task<IEnumerable<Category>> GetAllAsync()
        {
            return await _repo.GetAllAsync();
        }

        public async Task<Category?> GetByIdAsync(int id)
        {
            return await _repo.GetByIdAsync(id);
        }

        public async Task UpdateAsync(int id, CategoryCreateDto dto)
        {
            var category = await _repo.GetByIdAsync(id);
            if (category == null) throw new Exception("Category not found");

            category.CategoryName = dto.CategoryName;
            category.CategoryDescription = dto.CategoryDescription;

            await _repo.UpdateAsync(category);
        }

        public async Task DeleteAsync(int id)
        {
            await _repo.DeleteAsync(id);
        }
    }
}
