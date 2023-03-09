public static class Definitions
{
    // This is the name of the local file where creation date, map uid and PB
    // from every map in autosaves dir are stored. For example:local_autosaves_txt = "Autosaves_content.txt";
    public static string local_autosaves_txt = " ";

    // This is the Autosaves directory where replay gbx files are locally stored.
    public static string replays_path = @" ";

    // This is the working directory where any new txt files will be stored.
    // I set this one as the project's directory
    public static string working_path = @" ";
    
    // In case of a smb connection, the following parameters are required:

    // The remote computer's name or IP. For example: hostname = @"192.168.1.111";
    public static string hostname = @" ";
    
    // Your username for the remote computer
    public static string username = " ";
    
    // Your passowrd
    public static string password = @" ";
    
    // This is the sharename of the samba connection. If you connect via nautilus on a linux somputer
    // Then use one of the names in directory list which is higher in the hierarchy of the path
    // that the Autosaves dir is located. In this example User's home directory is shared, 
    // therefore sharename = @"username"; should work.
    public static string sharename = @" ";
    
    // This is the path to the Autosaves directory in the remote computer.
    // Supposing that home directory is shared (as above) the default path should be:
    // targetdir = @"Documents\Trackmania\Replays\Autosaves";
    public static string targetdir = @" ";

}
