using System.ComponentModel.DataAnnotations;

namespace Employee_proj.DTOs.Product
{
    public class ProductCreateDto
    {
        [Required]
        [RegularExpression(@"^[A-Za-z].*",
            ErrorMessage = "Product Name must start with a letter.")]
        public string ProductName { get; set; }

        [Range(1, int.MaxValue,
            ErrorMessage = "CategoryId must be greater than 0.")]
        public int CategoryId { get; set; }

        [Range(typeof(decimal), "0.01", "999999999")]
        public decimal Price { get; set; }

        [MaxLength(500)]
        public string? Description { get; set; }

        public IFormFile? Image { get; set; }
    }
}