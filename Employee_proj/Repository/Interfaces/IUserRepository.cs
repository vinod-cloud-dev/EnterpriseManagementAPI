using Employee_proj.Models;

namespace Employee_proj.Repository.Interfaces
{
    public interface IUserRepository
    {
        Task<User> GetByEmailAsync(string email);
        Task<User> GetByUserNamelAsync(string username);
        Task AddAsync(User user);
    }
}
