using Employee_proj.Models;

namespace Employee_proj.Jobs
{
    public class ProductCreatedJob
    {
        public void  Handle(int pid)
        {
             Console.WriteLine(   $"HANGFIRE JOB (BackGround ON everytime the product created is being called Product Created. Id = {pid}");
        }
    }
}
