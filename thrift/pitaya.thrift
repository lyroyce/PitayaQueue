
namespace php pitaya
namespace py pitaya 

enum Status {
	QUEUED		= 0,
	IN_PROGRESS	= 1,
	DONE		= 2,
	NOT_FOUND	= 10	
}

struct Message {
	1: optional Status status,
	8: optional string result 
}

struct Job {
	1: optional i32 id,
    	2: optional string payload,
	5: optional i32 queueTime,
	6: optional i32 startTime,
	7: optional i32 endTime
}

service Pitaya {

	Job queue(1: string payload), 

	Message query(1: i32 job_id),

	Job take(1: i32 timeout),

	void done(1: i32 job_id, 2: string result),

	oneway void shutdown()

}


