#include <java-utils/java_symbols.hpp>

using namespace fedora::java::javapackages::java_utils::java_symbols;

int main(int argc, const char** argv)
{
    std::span<const char*> args(argv + 1, argc - 1);
    
    auto parameter_dict = parse_arguments(args, {"-a", "--dry-run"});
    
    std::string default_root[] = {"."};
    
    std::span<std::string> fileroots = default_root;
    
    const auto parameters = interpret_args(parameter_dict);
    
    if (auto it = parameter_dict.find(""); it != parameter_dict.end())
    {
        fileroots = it->second;
    }
    
    #pragma omp parallel
    #pragma omp single
    for (const auto& fileroot : fileroots)
    {
        auto to_handle = std::filesystem::directory_entry(std::filesystem::path(fileroot));
        
        if (to_handle.is_regular_file())
        {
            #pragma omp task
            handle_file(std::move(to_handle), parameters);
        }
        else
        {
            for (auto& dir_entry : std::filesystem::recursive_directory_iterator(fileroot))
            {
                to_handle = std::move(dir_entry);
                if (to_handle.is_regular_file() and to_handle.path().native().ends_with(".java"))
                {
                    #pragma omp task
                    handle_file(std::move(to_handle), parameters);
                }
            }
        }
    }
}
