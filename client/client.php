<?php
require_once __DIR__.'/base/Client.php';
use pitaya\Status;

$client = new Client('localhost', '9908');
if(!$client->connect()){
	echo "Failed to connect to server.\n";
	exit;
} 
echo "Ready to queue a job...\n";
$job=$client->queue('This is a test job from client');
echo "The job is accepted by the server:\n";
print_r($job);
do{
	sleep(2);
	$message = $client->query($job->id);	
	if($message->status===Status::QUEUED){
		echo '=';
		
	}else if($message->status===Status::DONE){
		echo "Done\n".$message->result."\n";
	}else{
		echo ".";
	}
}while($message->status!==Status::DONE);

$client->disconnect();
