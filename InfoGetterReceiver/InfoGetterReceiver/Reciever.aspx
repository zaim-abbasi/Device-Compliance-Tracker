<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Reciever.aspx.cs" Inherits="InfoGetterReceiver.Reciever" %>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>Data Receiver</title>
    <style>
        #dataContainer {
            border: 1px solid #ccc;
            padding: 10px;
            width: 100%;
            height: 300px; /* Fixed height */
            overflow-y: scroll; /* Enable vertical scroll */
        }
    </style>
    <script src="Scripts/jquery-3.6.0.min.js"></script>
    <script src="Scripts/jquery.signalR-2.4.3.min.js"></script>
    <script src="signalr/hubs"></script>
    <script type="text/javascript">
        $(function () {
            // Reference the auto-generated proxy for the hub.
            var dataHub = $.connection.dataHub;

            // Create a function that the hub can call to broadcast messages.
            dataHub.client.updateData = function (data) {
                var formattedData = "<strong>System Info:</strong><br />";
                var systemInfo = data.system_info;
                for (var key in systemInfo) {
                    formattedData += key + ": " + systemInfo[key] + "<br />";
                }

                formattedData += "<strong>Network Info:</strong><br />";
                var networkInfo = data.network_info;
                for (var key in networkInfo) {
                    formattedData += key + ": " + networkInfo[key] + "<br />";
                }

                formattedData += "<strong>Hardware Info:</strong><br />";
                var hardwareInfo = data.hardware_info;
                for (var key in hardwareInfo) {
                    formattedData += key + ": " + hardwareInfo[key] + "<br />";
                }

                formattedData += "<strong>Installed Applications:</strong><br />";
                var installedApps = data.installed_apps;
                for (var i = 0; i < installedApps.length; i++) {
                    formattedData += installedApps[i] + "<br />";
                }

                $("#lblData").html(formattedData);
            };

            // Start the connection.
            $.connection.hub.start().done(function () {
                console.log("SignalR connection established.");
            });
        });
    </script>
</head>
<body>
    <form id="form1" runat="server">
        <div>
            <h2>Data Received</h2>
            <asp:Panel ID="dataContainer" runat="server">
                <asp:Label ID="lblData" runat="server" Text=""></asp:Label>
            </asp:Panel>
        </div>
    </form>
</body>
</html>