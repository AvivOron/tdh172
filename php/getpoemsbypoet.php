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

$poetID = $_POST["poetID"];
$sql = "SELECT * FROM poems where poet_id = '$poetID'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row

    //echo "<select id='poems' onchange='fetchPoem(this.value, this.options[this.selectedIndex].innerHTML)'>";
    //echo "<option>בחר שיר</option>";

    while($row = mysqli_fetch_array($result))
    { 
                      echo "<tr>";
                      echo "<td>";
                      echo "<a href='javascript:fetchPoem(". $row['id'] . ",\"" . $row['name'] . "\");'>" . $row['name'] . "</a>";
                      echo "</td>";
                      echo "</tr>";
    }

    //echo "</select>";
    //echo "</td>";


    while($row = $result->fetch_assoc()) {
        echo "id: " . $row["id"]. " - Name: " . $row["firstname"]. " " . $row["lastname"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>

