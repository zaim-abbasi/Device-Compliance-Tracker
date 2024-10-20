using Microsoft.AspNet.SignalR;
using System.Collections.Generic;
using System.Net;
using System.Net.Http;
using System.Web.Http;
using static InfoGetterReceiver.Reciever;

namespace InfoGetterReceiver
{
    public class ReceiverController : ApiController
    {
        [HttpPost]
        public IHttpActionResult PostData([FromBody] Dictionary<string, object> data)
        {
            if (data == null)
            {
                return BadRequest("Invalid data.");
            }

            // Process the data here
            // For example, you can add it to a static list or perform some actions
            Reciever.AddReceivedData(data); // Assuming you have a method to add data

            // Optionally notify clients using SignalR
            var context = GlobalHost.ConnectionManager.GetHubContext<DataHub>();
            context.Clients.All.updateData(data);

            return Ok(); // Respond with HTTP 200 OK
        }
    }
}
