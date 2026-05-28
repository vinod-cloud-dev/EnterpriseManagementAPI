using Employee_proj.DTOs.Category;
using Employee_proj.Models;
using Employee_proj.Repository.Interfaces;
using Employee_proj.Services.Interfaces;

namespace Employee_proj.Services.Implementations
{
    public class CategoryService : ICategoryService
    {
        private readonly ICategoryRepository _repo;
        private readonly ICacheService _cache;
        public CategoryService(ICategoryRepository repo, ICacheService cache)
        {
            _repo = repo;
            _cache = cache;
        }
        public async Task<Category> CreateAsync(CategoryCreateDto dto)
        {
            var category = new Category
            {
                CategoryName = dto.CategoryName,
                CategoryDescription = dto.CategoryDescription
            };
            await _repo.AddAsync(category);
            // ❗ Clear list cache
            await _cache.RemoveAsync("category_all");
            return category;
        }
        public async Task<IEnumerable<Category>> GetAllAsync()
        {
            string cacheKey = "category_all";
            var cachedList = await _cache.GetAsync<IEnumerable<Category>>(cacheKey);
            if (cachedList != null)
                return cachedList;
            var categories = await _repo.GetAllAsync();
            await _cache.SetAsync(cacheKey, categories);
            return categories;
        }
        public async Task<Category?> GetByIdAsync(int id)
        {
            string cacheKey = $"category_{id}";
            // 1. Try cache
            var cachedCategory = await _cache.GetAsync<Category>(cacheKey);
            if (cachedCategory != null)
                return cachedCategory;
            // 2. If not in cache → DB call
            // 👇 ADD THIS
            Console.WriteLine($"DB HIT: category_{id}");
            var category = await _repo.GetByIdAsync(id);

            if (category != null)
            {
                // 3. Store in cache
                await _cache.SetAsync(cacheKey, category);
            }
            return category;
        }
        public async Task UpdateAsync(int id, CategoryCreateDto dto)
        {
            var category = await _repo.GetByIdAsync(id);
            if (category == null) throw new Exception("Category not found");

            category.CategoryName = dto.CategoryName;
            category.CategoryDescription = dto.CategoryDescription;

            await _repo.UpdateAsync(category);

            // ❗ Remove specific + list cache
            await _cache.RemoveAsync($"category_{id}");
            await _cache.RemoveAsync("category_all");
        }
        public async Task DeleteAsync(int id)
        {
            await _repo.DeleteAsync(id);

            // ❗ Remove cache
            await _cache.RemoveAsync($"category_{id}");
            await _cache.RemoveAsync("category_all");
        }
    }
}
