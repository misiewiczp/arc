#include <math.h>
#include <chrono>
#include <iostream>
#include <thread>
#include <vector>
#include "Eigen-3.3/Eigen/Core"
#include "Eigen-3.3/Eigen/QR"
#include "MPC.h"
#include<sys/time.h>
#include <lcm/lcm-cpp.hpp>
#include <arc/req_plan_mpc_t.hpp>
#include <arc/res_plan_mpc_t.hpp>


// for convenience
using std::cout;
using std::endl;
using Eigen::VectorXd;
//using namespace std::chrono;

// For converting back and forth between radians and degrees.
constexpr double pi() { return M_PI; }
double deg2rad(double x) { return x * pi() / 180; }
double rad2deg(double x) { return x * 180 / pi(); }

// Evaluate a polynomial.
double polyeval(Eigen::VectorXd coeffs, double x) {
  double result = 0.0;
  for (int i = 0; i < coeffs.size(); i++) {
    result += coeffs[i] * pow(x, i);
  }
  return result;
}

// Fit a polynomial.
// Adapted from
// https://github.com/JuliaMath/Polynomials.jl/blob/master/src/Polynomials.jl#L676-L716
Eigen::VectorXd polyfit(Eigen::VectorXd xvals, Eigen::VectorXd yvals,
                        int order) {
  assert(xvals.size() == yvals.size());
  assert(order >= 1 && order <= xvals.size() - 1);
  Eigen::MatrixXd A(xvals.size(), order + 1);

  for (int i = 0; i < xvals.size(); i++) {
    A(i, 0) = 1.0;
  }

  for (int j = 0; j < xvals.size(); j++) {
    for (int i = 0; i < order; i++) {
      A(j, i + 1) = A(j, i) * xvals(j);
    }
  }

  auto Q = A.householderQr();
  auto result = Q.solve(yvals);
  return result;
}

int do_mpc(MPC &mpc, double &steer_value, double &throttle_value, 
	    vector<double> &mpc_x_vals, vector<double> &mpc_y_vals,
	    double px, double py, double psi, double v,
	    const vector<double> &ptsx, const vector<double> &ptsy)
{
          // Affine transformation. Consider car's orientation
          int waypoints_number = ptsx.size();
          VectorXd vehicle_waypoints_x(waypoints_number);
          VectorXd vehicle_waypoints_y(waypoints_number);
          for (int i = 0; i < waypoints_number; i++) {
            double diff_x = ptsx[i] - px;
            double diff_y = ptsy[i] - py;
            vehicle_waypoints_x[i] = diff_x * cos(-psi) - diff_y * sin(-psi);
            vehicle_waypoints_y[i] = diff_y * cos(-psi) + diff_x * sin(-psi);
          }
          auto coeffs = polyfit(vehicle_waypoints_x, vehicle_waypoints_y, 3);
          double cte = polyeval(coeffs, 0);
          double epsi = -atan(coeffs[1]);

          Eigen::VectorXd state(6);
          // Car's coordinate
          state << 0, 0, 0, v, cte, epsi;
          // Pass current state, reference trajectory's coefficients and get next actuator inputs
          // T is determined in MPC module
          auto vars = mpc.Solve(state, coeffs);
          steer_value = vars[0];
          throttle_value = vars[1];

          for (int i = 2; i < vars.size(); i++) {
            if (i%2 == 0) {
              mpc_x_vals.push_back(vars[i]);
            }
            else {
              mpc_y_vals.push_back(vars[i]);
            }
          }
	return 0;
}



lcm::LCM _lcm;


class MPCHandler {

    MPC mpc;

    public:
	~MPCHandler() {}

    void handleMessage(const lcm::ReceiveBuffer* rbuf,const std::string& chan, const arc::req_plan_mpc_t* msg)
    {
	arc::res_plan_mpc_t res;
	double steer_value = msg->dir;
	double throttle_value = msg->acc;

	vector<double> mpc_x_vals, mpc_y_vals;

	do_mpc(mpc, steer_value, throttle_value, 
	    res.points_x, res.points_y, msg->x, msg->y, msg->yaw, msg->vel, msg->points_x, msg->points_y);

	res.delta_dir = steer_value;
	res.delta_acc = throttle_value;
	res.npoints = res.points_x.size();

	res.req_timestamp = msg->timestamp;
	struct timeval tp;
	gettimeofday(&tp, NULL);
	long int mili = tp.tv_sec * 1000 + tp.tv_usec / 1000;
	res.timestamp = mili; //duration_cast< miliseconds >( system_clock::now().time_since_epoch() );
	
	_lcm.publish("MPC_RES", &res);
    }

};


int main(int argc, char *argv[]) {

  if (!_lcm.good())
    return 1;


  MPCHandler handlerObject;
  _lcm.subscribe("MPC_REQ", &MPCHandler::handleMessage, &handlerObject);
  while(0 == _lcm.handle());

  return 0;
}


/*
int main(int argc, char *argv[]) {
  MPC mpc;

  if (argc < 9){
     printf("Usage: current_steer_val current_throttle_val x y psi_orientation velocity way_point_1_x way_point_1_y ...\n");
     return 1;
  }
    int idx = 1;
    double steer_value = atof(argv[idx++]);
    double throttle_value = atof(argv[idx++]); 
    double px = atof(argv[idx++]);
    double py = atof(argv[idx++]);
    double psi = atof(argv[idx++]);
    double v = atof(argv[idx++]);
    
    vector<double> ptsx;
    vector<double> ptsy;

    // idx == 7
    for (; idx < argc; idx++) {
	if (idx%2 == 1) {
              ptsx.push_back(atof(argv[idx]));
        }
        else {
              ptsy.push_back(atof(argv[idx]));
        }
     }


    vector<double> mpc_x_vals, mpc_y_vals;

    do_mpc(mpc, steer_value, throttle_value, 
	    mpc_x_vals, mpc_y_vals, px, py, psi, v, ptsx, ptsx);

    cout << "Steer: "<< steer_value << "Throttle: " << throttle_value << endl;

    for(int i = 0; i < mpc_x_vals.size(); i++)
	cout << "MPC["<< i+1<< "]: " << mpc_x_vals[i]<< "," <<  mpc_y_vals[i]<< endl;

    return 0;
}
*/
