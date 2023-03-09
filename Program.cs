using static GBXFunctions;
internal partial class Program
{
    public static void Main(string[] args)
    {
        // Report of elapsing time may be omitted
        DateTime now = DateTime.Now;
        Console.WriteLine("start: " + now);
        long now_s = new DateTimeOffset(now).ToUnixTimeSeconds();

        if (args.Length == 0)

            // No arguments. The Autosaves database is located on the same disk
            GET_GBX_locally();

        else if (args[0] == "remote")

            // "remote" argument implies thtat the Autosaves dir is located on a different computer accessed via smb protocol
            GET_GBX_samba();
        else
        {
            Console.WriteLine("Wrong arguments");
        }
        
        // Report of elapsing time may be omitted
        now = DateTime.Now;
        long now_f = new DateTimeOffset(now).ToUnixTimeSeconds();
        Console.WriteLine("finish: " + now);
        Console.WriteLine("Total time in seconds: " + (now_f - now_s));
    }

}