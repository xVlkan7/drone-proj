// goal of this file:
// step 1: wait 100ms
// step 2: compute x = sin(t) and y = cos(t)
// step 3: publish point

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/geometry_msgs/msg/point.hpp>

#include <chrono>
#include <cmath>

using namespace std::chrono_literals;

class TargetPublisher : public rclcpp::Node
{
public:
    TargetPublisher();

private:
    void timerCallback();

    rclcpp::Publisher<geometry_msgs::msg::Point>::SharedPtr publisher_;

    rclcpp::TimerBase::SharedPtr timer_;

    rclcpp::Time start_time_;
};