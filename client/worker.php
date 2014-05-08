<?php
require_once __DIR__.'/base/Worker.php';

Class SimpleWorker extends Worker {

	public function work($job){
		echo "Working on a new job:\n";
		print_r($job);
		sleep(5);
		echo "Done\n";
		return "This is a result from worker";
	}
}
$worker = new SimpleWorker('localhost', '9908');
$worker->start();
