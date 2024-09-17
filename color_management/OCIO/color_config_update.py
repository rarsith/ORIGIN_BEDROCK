import os

# Path to your color.ocio file
ocio_file_path = "D:\\__REPOSITORIES\\Installs\\openColorIO\\OpenColorIO-Configs-feature-aces-1.2-config\\aces_1.2\\config.ocio"

# IDT settings for DJI Air3 (D-Log)
idt_name = "IDT_DJI_Air3_DLog"
idt_description = "Input Device Transform for DJI Air3 using D-Log"
idt_transform = "D:\\__REPOSITORIES\\Installs\\openColorIO\\OpenColorIO-Configs-feature-aces-1.2-config\\aces_1.2\\custom_luts\\DJI_Air3_DLog_to_ACES.spi1d\\DJI_Air3_DLog_to_ACES.spi1d"

# Function to add the IDT to the .ocio file
def add_idt_to_ocio(ocio_file_path, idt_name, idt_description, idt_transform):
    with open(ocio_file_path, 'r') as file:
        lines = file.readlines()

    # Find the location where new IDTs should be added
    for i, line in enumerate(lines):
        if "roles:" in line:
            idx = i
            break

    # Create the IDT configuration string
    idt_config = f"\n- !<ColorSpace>\n  name: {idt_name}\n  family: IDT\n  equalitygroup: \"\"\n  bitdepth: 32f\n  description: {idt_description}\n  isdata: false\n  allocation: uniform\n  to_reference: !<FileTransform> {{src: \"{idt_transform}\", interpolation: linear}}\n"

    # Insert the new IDT
    lines.insert(idx, idt_config)

    # Write back to the .ocio file
    with open(ocio_file_path, 'w') as file:
        file.writelines(lines)

    print(f"IDT {idt_name} added successfully.")

# Run the function to add IDT
add_idt_to_ocio(ocio_file_path, idt_name, idt_description, idt_transform)
