using System.Net;
using System.Text;
using GBX.NET;
using GBX.NET.LZO;
using GBX.NET.Engines.Game;
using SMBLibrary;
using SMBLibrary.Client;

public partial class GBXFunctions
{
    public static void GET_GBX_samba()
    {
        object directoryHandle;
        object fileHandle;
        var list_of_files = new List<string>();
        var list_of_dates = new List<long>();
        DateTime modified_on;
        
        // The name of the file where data from Autosaves dir files are stored
        string autosaves_content_file = Definitions.working_path + Definitions.local_autosaves_txt;

        // If the Autosaves_content.txt file exists, then delete it
        if (File.Exists(autosaves_content_file))
            File.Delete(autosaves_content_file);

        // Create the Autosaves_content.txt file and write the first line with the column headers
        FileStream autosaves = File.Create(autosaves_content_file);
        AddText(autosaves, "unix_date,map_ID,PB_ms\n");


        // The following lines implement the CLientExamples of the SMBLIbrary git repository.
        // It can be found here: https://github.com/TalAloni/SMBLibrary/blob/master/ClientExamples.md
        SMB2Client client = new SMB2Client(); // SMB2Client can be used as well
        bool isConnected = client.Connect(IPAddress.Parse(Definitions.hostname), SMBTransportType.DirectTCPTransport);
        if (isConnected)
        {
            NTStatus status = client.Login(String.Empty, Definitions.username, Definitions.password);
            if (status == NTStatus.STATUS_SUCCESS)
            {
                        
                List<string> shares = client.ListShares(out status); 

                ISMBFileStore fileStore = client.TreeConnect(Definitions.sharename, out status);
                if (status == NTStatus.STATUS_SUCCESS)
                {
                    FileStatus fileStatus;
                    status = fileStore.CreateFile(out directoryHandle, out fileStatus, Definitions.targetdir, AccessMask.GENERIC_READ, SMBLibrary.FileAttributes.Directory, ShareAccess.Read | ShareAccess.Write, CreateDisposition.FILE_OPEN, CreateOptions.FILE_DIRECTORY_FILE, null);
                    if (status == NTStatus.STATUS_SUCCESS)
                    {
                        // The first operation creates two lists: 
                        // a) a list with the filenames inside the Autosaves directory
                        // b) a list with the date (in milliseconds since Epoch) that the .gbx file is modified.
                        List<QueryDirectoryFileInformation> fileList;
                        status = fileStore.QueryDirectory(out fileList, directoryHandle, "*", FileInformationClass.FileDirectoryInformation);

                        foreach (QueryDirectoryFileInformation file in fileList)
                        {
                            if (((((SMBLibrary.FileDirectoryInformation)file).FileName)!=".") & ((((SMBLibrary.FileDirectoryInformation)file).FileName)!=".."))
                            {                    
                                list_of_files.Add(((SMBLibrary.FileDirectoryInformation)file).FileName);
                                modified_on = (((SMBLibrary.FileDirectoryInformation)file).LastWriteTime);
                                long date_unix = new DateTimeOffset(modified_on).ToUnixTimeSeconds();
                                list_of_dates.Add(date_unix);
                            }
                        }
                        status = fileStore.CloseFile(directoryHandle);
                    }

                    // initiate a counter for a console report of total files
                    int i = 0;

                    // The second operation streams the gbx file to the local computer, stores it locally and reads the header.
                    foreach (string file_to_open in list_of_files)
                    {
                        string filepath = Definitions.targetdir + @"\" + file_to_open;
                        status = fileStore.CreateFile(out fileHandle, out fileStatus, filepath, AccessMask.GENERIC_READ | AccessMask.SYNCHRONIZE, SMBLibrary.FileAttributes.Normal, ShareAccess.Read, CreateDisposition.FILE_OPEN, CreateOptions.FILE_NON_DIRECTORY_FILE | CreateOptions.FILE_SYNCHRONOUS_IO_ALERT, null);
                        if (status == NTStatus.STATUS_SUCCESS)
                        {
                            // The gbx file is streamed vis smb protocol to the local computer
                            System.IO.MemoryStream stream = new System.IO.MemoryStream();
                            byte[] data;
                            long bytesRead = 0;
                            while (true)
                            {
                                status = fileStore.ReadFile(out data, fileHandle, bytesRead, (int)client.MaxReadSize);
                                if (status != NTStatus.STATUS_SUCCESS && status != NTStatus.STATUS_END_OF_FILE)
                                {
                                    throw new Exception("Failed to read from file");
                                }

                                if (status == NTStatus.STATUS_END_OF_FILE || data.Length == 0)
                                {
                                    break;
                                }
                                bytesRead += data.Length;
                                stream.Write(data, 0, data.Length);
                            }

                            // Deletes "temp.gbx"
                            if (File.Exists("temp.gbx"))
                                File.Delete("temp.gbx");
                            
                            // Streamed data are stored to the "temp.gbx"
                            FileStream file = new FileStream("temp.gbx", FileMode.Create, FileAccess.Write);
                            stream.WriteTo(file);
                            file.Close();
                            stream.Close();

                             // Get the file's header into the proper class
                            GameBox.LZO = new MiniLZO();
                            var node = GameBox.ParseNode("temp.gbx");
                            switch (node)
                            {
                                case CGameCtnReplayRecord replay:
                                    if (replay.MapInfo is not null)
                                    {
                                        // Add to Autosaves_content.txt file: file modification date, map ID and PB time in milliseconds.
                                        string line = string.Format("{0},{1},{2}\n", list_of_dates[i], replay.MapInfo.Id, replay.Time?.TotalMilliseconds);
                                        AddText(autosaves, line);
                                    }
                                break;

                            }
                        status = fileStore.CloseFile(fileHandle);
                        }
                        // increment the counter
                        i++;
                    }
                    // Report number of files
                    Console.WriteLine("Total files processed: " + i);

                    // Close the local Autosaves content txt file
                    autosaves.Close();
                }
                status = fileStore.Disconnect();

                // Delete "temp.gbx"
                File.Delete("temp.gbx");
            }
            client.Logoff();
        }
        client.Disconnect();
    }
}
