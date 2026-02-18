namespace Employee_proj.DTOs.Product
{
    public class ProductCreateDto
    {
        public string ProductName { get; set; }
        public int CategoryId { get; set; }
        public decimal Price { get; set; }
        public string? Description { get; set; }
        public IFormFile? Image { get; set; }
    }
}
