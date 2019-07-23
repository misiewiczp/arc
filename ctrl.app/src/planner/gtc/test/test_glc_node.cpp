/* Copyright (C) Brian Paden (bapaden@mit.edu)
 * Written by Brian Paden
 * Released under the MIT License
 */

#include<glc_node.h>
#include<gtest/gtest.h>

using namespace glc;

/**
 * This test checks the following properties of a Node:
 * 1) That the merit attribute is set to the some of cost with the estimated cost-to-go
 * 2) That the merit of child is greater than root since root has less cost plus heuristic
 * 3) That the parent attribute in child points to the root node 
 */
TEST(GlcNode,Order){
  std::shared_ptr<const Node> root = std::shared_ptr<const Node>(new Node(5,0,10.0,10.0,std::valarray<double>({0.0,1.0}),1.0,nullptr,nullptr,nullptr));
  std::shared_ptr<const Node> child = std::shared_ptr<const Node>(new Node(4,1,8.0,14.0,std::valarray<double>({1.0,1.0}),1.0,nullptr,nullptr,nullptr));
  
  NodeMeritOrder comparator;
  
  EXPECT_EQ(root->merit,20.0);
  EXPECT_EQ(child->merit,22.0);
  EXPECT_FALSE(comparator(root,child));
  EXPECT_TRUE(comparator(child,root));
  
}

int main(int argc, char** argv){
  
  ::testing::InitGoogleTest(&argc,argv);
  return RUN_ALL_TESTS();
  
}
