using MailKit.Net.Smtp;
using MimeKit;
using Employee_proj.Services.Interfaces;

namespace Employee_proj.Services.Implementations
{
    public class EmailService : IEmailService
    {
        private readonly ILogger<EmailService> _logger;
        public EmailService(ILogger<EmailService> logger)
        {
            _logger = logger;
        }
        public async Task SendEmailAsync(string to, string subject, string body)
        {
            try
            {
                var email = new MimeMessage();
                email.From.Add(MailboxAddress.Parse("vinodpkoti810@gmail.com"));
                email.To.Add(MailboxAddress.Parse(to));
                email.Subject = subject;
                email.Body = new TextPart("html")
                {
                    Text = body
                };
                using var smtp = new SmtpClient();
                await smtp.ConnectAsync("smtp.gmail.com",587,MailKit.Security.SecureSocketOptions.StartTls);
                await smtp.AuthenticateAsync("vinodpkoti810@gmail.com","zfwhygkhtfcmgzfp");
                await smtp.SendAsync(email);
                _logger.LogInformation("Email sent successfully to {Email} at {Time}",to,DateTime.Now);
                await smtp.DisconnectAsync(true);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex,"Email failed for {Email} at {Time}",to,DateTime.Now);
                throw;
            }
        }
    }
}