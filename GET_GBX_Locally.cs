using System.Text;
using GBX.NET;
using GBX.NET.Engines.Game;


public partial class GBXFunctions
{
    public static void GET_GBX_locally()
    {
        // The name of the file where data from Autosaves dir files will be stored
        string autosaves_content_file = Definitions.working_path + Definitions.local_autosaves_txt;

        // If the Autosaves_content.txt file exists, then delete it
        if (File.Exists(autosaves_content_file))
            File.Delete(autosaves_content_file);

        // Create the Autosaves_content.txt file and write the first line with the column headers
        FileStream autosaves = File.Create(autosaves_content_file);
        AddText(autosaves, "unix_date,map_ID,PB_ms\n");

        // initiate a counter for a console report of total files
        int i =0;

        // Retrieve data from each file in the Autosaves dir
        foreach (string file in Directory.GetFiles(Definitions.replays_path))
        {

            if (File.Exists(file))
            {
                // Retrieve modification date and turn it to Unix time in seconds
                DateTime file_modification_date = File.GetLastWriteTime(file);
                long date_unix = new DateTimeOffset(file_modification_date).ToUnixTimeSeconds();

                // Get the file's header into the proper class
                var node = GameBox.ParseNode(file);
                switch (node)
                {
                    case CGameCtnReplayRecord replay:
                        if (replay.MapInfo is not null)
                        {
                            // Add to Autosaves_content.txt file: file modification date, map ID and PB time in milliseconds.
                            string line = string.Format("{0},{1},{2}\n", date_unix, replay.MapInfo.Id, replay.Time?.TotalMilliseconds);
                            AddText(autosaves, line);
                        }
                        break;

                }
            }
            // incerement the counter
            i++;
        }
        // Report number of files
        Console.WriteLine("Total files processed: " + i);

        // Close the local Autosaves content txt file
        autosaves.Close();
        
        
    }


    // I found this routine here: https://learn.microsoft.com/en-us/dotnet/api/system.io.filestream?view=net-7.0
    // Writes a string to a file
    public static void AddText(FileStream fs, string value)
    {
        byte[] info = new UTF8Encoding(true).GetBytes(value);
        fs.Write(info, 0, info.Length);
    }
}
