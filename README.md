# World Building System (WBS)

Welcome to the World Building System (WBS) repository. This project is designed to help authors and creators organize and manage the complex information required for creating detailed and immersive worlds. The WBS allows for hierarchical structuring of universes, galaxies, worlds, and stories, along with detailed components such as characters, items, locations, and lore.

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Status

This repo consists of some half-baked ideas and Proof of Concept implementations. Use at your own risk. No ongoing development or support should be assumed. 

## Features

- Hierarchical organization of universe, galaxy, world, and story levels.
- Detailed management of components including characters, items, locations, and lore.
- Human-readable directory and file structure.
- Version control integration with Git for collaboration and change tracking.
- Extensible for future development with narrative arcs and timelines.


## Directory Structure of the World Building System (WBS)

The World Building System (WBS) employs a hierarchical directory structure to organize and manage the various elements required for creating detailed and immersive worlds. This structure ensures that all elements are logically arranged and easily accessible.

### Directory Structure

#### 1. Level or Story Directory

Each level or story directory contains the following key elements:

- **settings.json**: Metadata about the current level or story, such as its name, description, authors, and version.

- **sublevels**: Contains directories for the next hierarchical levels (e.g., galaxies within a universe, worlds within a galaxy, stories within a world). This structure ensures consistency and scalability.

- **components**: Contains grouped components related to the current level or story. Components are organized into specific groups such as characters, items, locations, and lore. Each component group contains individual elements relevant to the story or level.

- **arcs**: Reserved for narrative arcs. This directory can be used to store files that detail narrative threads spanning multiple levels and stories.

- **timelines**: Reserved for timelines. This directory can be used to store files that track events and their chronological order within the world.

#### 2. Components Directory

The `components` directory within each level or story includes various organizational subdirectories for different types of components:

- **characters**: Contains individual character components.
- **items**: Contains individual item components.
- **locations**: Contains individual location components.
- **lore**: Contains individual lore components, which provide additional background and context to the world.

Each component is stored in its own directory, including files such as descriptions, images, and metadata.

### Summary

The hierarchical directory structure of the WBS ensures that all elements of world-building are well-organized, easily accessible, and scalable. This structure supports detailed and immersive world-building, facilitating the creation of rich and complex worlds.

## Contributing

Don't. 

I will assume any feedback including(but not limited to) suggestions, pull requests, &c. automatically assign any rights to me.

## License

None. This work is protected by Copyright.
