<?php
$servername = "tdh.cmq2zbutzn8e.us-west-2.rds.amazonaws.com";
$username = "bialik";
$password = "12345678";
$dbname = "tdh172";
error_reporting(E_ALL);
// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

  if (!$conn->set_charset("utf8")) {
      printf("Error loading character set utf8: %s\n", $conn->error);
  } else {
  }
  

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$poemID = $_POST["poemID"];
$dest1 = $_POST["dest1"];
$dest2 = $_POST["dest2"];
$sql = "SELECT p1.name as name, p1.original_data as original_data, p1.translated_data as translated_data, p2.name as poet_name, p2.wikipedia_url as url FROM poems p1 join poets p2 on p1.poet_id = p2.id where p1.id = '$poemID'";

$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row

    echo "<table>";
    

    while($row = mysqli_fetch_array($result))
    { 
    echo "<tr><td><b>" .  $row['name'] . " \ " . $row['poet_name'] . "</b></td><td style='padding-right:20px'>למידע נוסף אודות המשורר\ת <a target='_blank' href='" .  $row['url'] . "'>לחצ\י כאן</a><br></td></tr>";
    echo "<tr><td><br></td></tr>";
    echo "<tr>" ;
    echo "<td><div id='$dest1'>" . $row['original_data'] . "</div></td>";
    echo "<td style='padding-right:20px'><div id='$dest2'>" . $row['translated_data'] . "</div></td>";
    echo "</tr>" ;
    }

    
    echo "</table>";


    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["id"]. " - Name: " . $row["firstname"]. " " . $row["lastname"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>

