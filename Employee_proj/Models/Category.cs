using System.ComponentModel.DataAnnotations;

namespace Employee_proj.Models
{
    public class Category
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public string CategoryName { get; set; }

        public string? CategoryDescription { get; set; }

        public ICollection<Product> Products { get; set; }
    }
}
