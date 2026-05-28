using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;


namespace Employee_proj.Models
{
    public class Profile
    {
        public  int ID { get; set; }
         public string Name { get; set; }
        public  string Address { get; set; }
        public string Phone { get; set; }
        public int   UserId { get; set; }
        [ForeignKey("UserId")]
        public User User { get; set; }
    }
}
