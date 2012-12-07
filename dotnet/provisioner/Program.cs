﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Data.SqlClient;
using Microsoft.Synchronization;

namespace ConsoleApplication1
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length == 0)
            {
                Console.WriteLine("Wrong number of args");
                printUsage();
                return;
            }

            SqlConnection server = new SqlConnection();
            SqlConnection client = new SqlConnection();
            string serverconn = "";
            string clientconn = "";
            bool deprovison = false;
            string tablename = "";
            string direction = "Download";
            int srid = 0;

            bool hasserver = args.Any(x => x.Contains("--server"));
            if (!hasserver)
            {
                Console.Error.WriteLine("We need a server connection string");
                printUsage();
                return;
            }

            // If there is no client arg given then we assume that we are talking
            // working on the server tables
            bool hastable = args.Any(x => x.Contains("--table"));
            if (!hastable)
            {
                Console.Error.WriteLine("We need a table to work on");
                printUsage();
                return;
            }

            foreach (var arg in args)
            {
                Console.WriteLine(arg);
                var pairs = arg.Split(new char[] { '=' }, 2,
                                      StringSplitOptions.None);
                var name = pairs[0];
                string parm = "";
                if (pairs.Length == 2)
                    parm = pairs[1];
                switch (name)
                {
                    case "--server":
                        serverconn = parm;
                        server.ConnectionString = parm;
                        break;
                    case "--client":
                        clientconn = parm;
                        client.ConnectionString = parm;
                        break;
                    case "--table":
                        tablename = parm;
                        break;
                    case "--direction":
                        direction = parm;
                        break;
                    case "--deprovision":
                        deprovison = true;
                        break;
                    case "--srid":
                        srid = int.Parse(parm);
                        break;
                    default:
                        break;
                }
            }

            if (srid == 0)
            {
                Console.Error.WriteLine("We need a SRID");
                printUsage();
                return;
            }

            // If there is no client arg given then we assume that we are
            // working on the server tables
            bool hasclient = args.Any(x => x.Contains("--client"));
            if (!hasclient)
            {
                client = server;
                Console.WriteLine("No client given. Client is now server connection");
            }

            Console.WriteLine("\n\r");

            Console.WriteLine("Running using these settings");
            Console.WriteLine("Server:" + server.ConnectionString);
            Console.WriteLine("Client:" + client.ConnectionString);
            Console.WriteLine("Table:" + tablename);
            Console.WriteLine("Direction:" + direction);
            Console.WriteLine("Mode:" + (deprovison ? "Deprovison" : "Provision"));

            if (!deprovison)
            {
                Provisioning.ProvisionTable(server, client, tablename, srid);
                Console.WriteLine("Provision complete");
                if (server.ConnectionString != client.ConnectionString)
                {
                    Console.WriteLine("Adding to scopes table on client");
                    Provisioning.AddScopeToScopesTable(client, tablename,
                                                       utils.StringToEnum<SyncDirectionOrder>(direction));
                }
                Console.WriteLine("Complete");
            }
            else
            {
                Deprovisioning.DeprovisonScope(client, tablename);
                Console.WriteLine("Deprovision complete");
            }  

            Console.Read();
        }

        static void printUsage()
        {
            Console.WriteLine(@"provisioner --server={connectionstring} --table={tablename} --srid={SRID} [options]
[options]

--client={connectionstring} : The connection string to the client database. 
                              If blank will be set to server connection.
--direction=UploadAndDownload|DownloadAndUpload|Upload|Download : The direction that the table will sync.
                            if blank will be set to OneWay.
--deprovision : Deprovision the table rather then provision. WARNING: Will drop
                the table on the client if client and server are different! Never
                drops server tables.");
        }
    }
}
