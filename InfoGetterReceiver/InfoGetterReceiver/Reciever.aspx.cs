using System;
using System.Collections.Generic;
using System.IO;
using System.Web;
using System.Web.Script.Serialization;
using System.Web.Http;
using Microsoft.AspNet.SignalR;
using Owin;
using Microsoft.Owin;
using System.Net.Http;
using System.Threading.Tasks;
using System.Linq;
using System.Threading;

[assembly: OwinStartup(typeof(InfoGetterReceiver.Reciever))]
namespace InfoGetterReceiver
{
    public partial class Reciever : System.Web.UI.Page
    {
        private static List<string> receivedData = new List<string>();

        protected void Page_Load(object sender, EventArgs e)
        {
            // Remove the POST request handling code here
            lblData.Text = "Send a POST request to receive data.";
        }

        public static void AddReceivedData(Dictionary<string, object> data)
        {
            // Process and store the received data as needed
            receivedData.Add(new JavaScriptSerializer().Serialize(data));

            // Here you can format and store data as needed or display it
        }

        public class DataHub : Hub
        {
            public void Send(string message)
            {
                Clients.All.addMessage(message);
            }
        }

        public void Configuration(IAppBuilder app)
        {
            // Configure SignalR
            app.MapSignalR();

            // Configure the Web API middleware manually
            app.Use(typeof(WebApiMiddleware), new HttpConfiguration());

            // Handle requests to the Web API
            app.Use(async (context, next) =>
            {
                if (context.Request.Path.StartsWithSegments(new PathString("/api/receiver")))
                {
                    var httpRequestMessage = new HttpRequestMessage
                    {
                        Method = new HttpMethod(context.Request.Method),
                        RequestUri = new Uri(context.Request.Uri.AbsoluteUri),
                        Content = new StreamContent(context.Request.Body)
                    };

                    foreach (var header in context.Request.Headers)
                    {
                        httpRequestMessage.Headers.TryAddWithoutValidation(header.Key, header.Value.ToArray());
                    }

                    // Initialize Web API configuration
                    var config = new HttpConfiguration();
                    config.Routes.MapHttpRoute(
                        name: "DefaultApi",
                        routeTemplate: "api/{controller}/{id}",
                        defaults: new { id = RouteParameter.Optional }
                    );

                    // Create a new HttpServer using the configuration
                    var server = new HttpServer(config);
                    var handler = new HttpMessageHandlerAdapter(server);

                    // Send the request using the handler
                    var httpResponseMessage = await handler.SendAsync(httpRequestMessage, CancellationToken.None);

                    context.Response.StatusCode = (int)httpResponseMessage.StatusCode;
                    foreach (var header in httpResponseMessage.Headers)
                    {
                        context.Response.Headers.Append(header.Key, header.Value.ToArray());
                    }

                    await context.Response.WriteAsync(await httpResponseMessage.Content.ReadAsStringAsync());
                }
                else
                {
                    await next();
                }
            });
        }
    }

    public class WebApiMiddleware : OwinMiddleware
    {
        private readonly HttpConfiguration _config;

        public WebApiMiddleware(OwinMiddleware next, HttpConfiguration config) : base(next)
        {
            _config = config;
        }

        public override async Task Invoke(IOwinContext context)
        {
            await Next.Invoke(context);
        }
    }

    public class HttpMessageHandlerAdapter : HttpMessageHandler
    {
        private readonly HttpServer _server;

        public HttpMessageHandlerAdapter(HttpServer server)
        {
            _server = server;
        }

        protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            return await _server.SendAsync(request, cancellationToken);
        }
    }
}
