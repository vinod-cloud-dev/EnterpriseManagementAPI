using Employee_proj.Data;

namespace Employee_proj.Jobs
{
    public class ProductJobService
    {
        private readonly ApplicationDbContext _context;

        public ProductJobService(ApplicationDbContext context)
        {
            _context = context;
        }

        public void PrintProductCount()
        {
            var count = _context.Products.Count();

            Console.WriteLine($"[{DateTime.Now:yyyy-MM-dd HH:mm:ss}] Total Products: {count}");
        }
    }
}
