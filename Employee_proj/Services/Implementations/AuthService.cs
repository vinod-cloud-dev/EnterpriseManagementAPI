using Employee_proj.Repository.Interfaces;
using Employee_proj.Services.Interfaces;
using Microsoft.AspNetCore.Identity;
using Employee_proj.Models;
using Employee_proj.DTOs.Auth;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace Employee_proj.Services.Implementations
{
    public class AuthService : IAuthService
    {
        private readonly IUserRepository _userRepo;
        private readonly IConfiguration _configuration;
        private readonly PasswordHasher<User> _hasher;

        public AuthService(IUserRepository userRepo, IConfiguration configuration)
        {
            _userRepo = userRepo;
            _configuration = configuration;
            _hasher = new PasswordHasher<User>();
        }

        public async Task<string?> RegisterAsync(RegisterDto dto)
        {
            var existingUserEmail = await _userRepo.GetByEmailAsync(dto.Email.ToLower());
            if (existingUserEmail != null)
                return null;
            var exitingUserName = await _userRepo.GetByUserNamelAsync(dto.Username.ToLower());
            if (exitingUserName != null)
                return "2";
            var user = new User
            {
                Username = dto.Username,
                Email = dto.Email,
                Role = "User"
            };
            user.PasswordHash = _hasher.HashPassword(user, dto.Password);
            await _userRepo.AddAsync(user);
            return "User registered successfully";
        }

        public async Task<string?> LoginAsync(LoginDto dto)
        {
            var user = await _userRepo.GetByEmailAsync(dto.Email);
            if (user == null) return null;
            var result = _hasher.VerifyHashedPassword(user, user.PasswordHash, dto.Password);
            if (result == PasswordVerificationResult.Failed)
                return null;
            return GenerateToken(user);
        }
        private string GenerateToken(User user)
        {
            var claims = new[]
            {
            new Claim(ClaimTypes.Name, user.Email),
            new Claim(ClaimTypes.Role, user.Role)
        };

            var key = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(_configuration["Jwt:Key"]));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
            var token = new JwtSecurityToken(
                issuer: _configuration["Jwt:Issuer"],
                audience: _configuration["Jwt:Audience"],
                claims: claims,
                expires: DateTime.Now.AddMinutes(60),
                signingCredentials: creds);
            return new JwtSecurityTokenHandler().WriteToken(token);
        }


    }
}
