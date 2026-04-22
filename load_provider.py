import importlib

def load_provider(module_path, class_name):
    """
    Dynamically import a provider class given its module path and class name.
    Example:
        provider = load_provider(
            'wi_crash_engine.providers.milwaukee_pd', 'MilwaukeePDProvider')
    """
    module = importlib.import_module(module_path)
    provider_class = getattr(module, class_name)
    return provider_class

if __name__ == "__main__":
    # Example usage
    ProviderClass = load_provider(
        'wi_crash_engine.providers.milwaukee_pd', 'MilwaukeePDProvider')
    provider = ProviderClass(api_key='YOUR_API_KEY')
    print(provider)
