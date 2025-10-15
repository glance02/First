CXX = g++
CXXFLAGS = -Wall -std=c++11

# 正确的目标规则：从 .cpp 生成可执行文件
%: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	del *.exe 2>nul || true
